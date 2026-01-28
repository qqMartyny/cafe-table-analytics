package com.cafe.storage.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "occupancy_period")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class OccupancyPeriod {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "analysis_task_id", nullable = false)
    @ToString.Exclude
    @EqualsAndHashCode.Exclude
    private AnalysisTask analysisTask;

    @Column(name = "table_id", nullable = false)
    private Integer tableId;
    
    @Column(name = "period_start_seconds", nullable = false)
    private Float periodStartSeconds;
    
    @Column(name = "period_end_seconds", nullable = false)
    private Float periodEndSeconds;
    
    @Column(name = "is_occupied", nullable = false)
    private Boolean isOccupied;
    
    @Column(name = "duration_seconds", nullable = false)
    private Float durationSeconds;
}
