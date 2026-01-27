"""
Анализатор занятости столов
"""

from collections import deque
import numpy as np


class OccupancyAnalyzer:
    def __init__(self, tables_config, occupied_frames=3, free_frames=2):
        """
        Args:
            tables_config: dict с конфигурацией столов из JSON
            occupied_frames: кол-во кадров подряд для определения занятости
            free_frames: кол-во кадров подряд для определения освобождения
        """
        self.tables = tables_config['tables']
        self.occupied_threshold = occupied_frames
        self.free_threshold = free_frames
        
        # История состояний для каждого стола (последние N кадров)
        self.frame_history = {
            table['id']: deque(maxlen=max(occupied_frames, free_frames))
            for table in self.tables
        }
        
        # Текущее состояние каждого стола
        self.current_state = {table['id']: False for table in self.tables}
        
        print(f"Инициализирован анализатор для {len(self.tables)} столов")
        print(f"Правила: {occupied_frames} кадров → занят, {free_frames} кадров → свободен")
    
    def analyze_frame(self, people_detections):
        """
        Анализ занятости столов на текущем кадре
        
        Args:
            people_detections: список людей от PersonDetector
        
        Returns:
            dict: {table_id: {'occupied': bool, 'people_count': int, 'state_changed': bool}}
        """
        results = {}
        
        for table in self.tables:
            table_id = table['id']
            bbox = table['bbox']
            
            # Создаём расширенную зону для детекции сидящих
            seating_zone = self._create_seating_zone(bbox)
            
            # Находим людей в зоне стола
            people_in_zone = self._find_people_in_zone(
                people_detections, 
                seating_zone
            )
            
            # Определяем есть ли сидящие люди
            has_people = len(people_in_zone) > 0
            
            # Добавляем в историю
            self.frame_history[table_id].append(has_people)
            
            # Применяем временной фильтр
            previous_state = self.current_state[table_id]
            new_state = self._apply_temporal_filter(table_id)
            self.current_state[table_id] = new_state
            
            results[table_id] = {
                'occupied': new_state,
                'people_count': len(people_in_zone),
                'raw_detections': len(people_in_zone),
                'state_changed': previous_state != new_state,
                'people_in_zone': people_in_zone  # для отладки
            }
        
        return results
    
    def _create_seating_zone(self, table_bbox, margin=100):
        """
        Создаём расширенную зону вокруг стола для детекции сидящих
        
        Args:
            table_bbox: {'x1': int, 'y1': int, 'x2': int, 'y2': int}
            margin: отступ в пикселях
        
        Returns:
            (x1, y1, x2, y2)
        """
        return (
            table_bbox['x1'] - margin,
            table_bbox['y1'] - margin,
            table_bbox['x2'] + margin,
            table_bbox['y2'] + margin
        )
    
    def _find_people_in_zone(self, people_detections, zone):
        """
        Находим людей, центр которых находится в зоне
        
        Args:
            people_detections: список от PersonDetector
            zone: (x1, y1, x2, y2)
        
        Returns:
            list: отфильтрованный список людей
        """
        zx1, zy1, zx2, zy2 = zone
        
        people_in_zone = []
        
        for person in people_detections:
            cx, cy = person['center']
            
            # Проверяем что центр человека в зоне
            if zx1 <= cx <= zx2 and zy1 <= cy <= zy2:
                people_in_zone.append(person)
        
        return people_in_zone
    
    def _apply_temporal_filter(self, table_id):
        """
        Применяем правила временной фильтрации
        
        Правила:
        - Занят: если последние N кадров подряд есть люди
        - Свободен: если последние M кадров подряд нет людей
        - Иначе: сохраняем предыдущее состояние (гистерезис)
        """
        history = list(self.frame_history[table_id])
        
        if len(history) == 0:
            return False
        
        # Правило занятости
        if len(history) >= self.occupied_threshold:
            recent = history[-self.occupied_threshold:]
            if all(recent):  # все последние N кадров = True
                return True
        
        # Правило освобождения
        if len(history) >= self.free_threshold:
            recent = history[-self.free_threshold:]
            if not any(recent):  # все последние M кадров = False
                return False
        
        # Гистерезис - сохраняем текущее состояние
        return self.current_state[table_id]
    
    def get_statistics(self):
        """Получить текущую статистику по всем столам"""
        total_tables = len(self.tables)
        occupied_tables = sum(1 for state in self.current_state.values() if state)
        
        return {
            'total_tables': total_tables,
            'occupied': occupied_tables,
            'free': total_tables - occupied_tables,
            'occupancy_rate': occupied_tables / total_tables if total_tables > 0 else 0
        }