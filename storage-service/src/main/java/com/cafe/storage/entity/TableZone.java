package com.cafe.storage.entity;

import lombok.*;
import jakarta.persistence.*;

@Entity
@Table(name = "table_zones")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TableZone {
    
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

    @Column(name = "bbox_x1", nullable = false)
    private Float bboxX1;

    @Column(name = "bbox_x2", nullable = false)
    private Float bboxX2;

    @Column(name = "bbox_y1", nullable = false)
    private Float bboxY1;

    @Column(name = "bbox_y2", nullable = false)
    private Float bboxY2;

}
