package com.cafe.storage.entity;

import java.time.LocalDateTime;
import java.util.List;
import java.util.ArrayList;

import org.hibernate.mapping.Array;
import org.springframework.cglib.core.Local;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "Analysis_tasks")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AnalysisTask {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "video_filename", nullable = false, length = 500)
    private String videoFilename;

    @Column(name = "ml_task_id", unique = true)
    private String mlTaskId;

    @Column(name = "status", nullable = false, length = 50)
    private String status;

    @Column(name = "ctreated_at", nullable = false)
    private LocalDateTime createdAt;

    @Column(name = "completed_at")
    private LocalDateTime completedAt;

    @Column(name = "total_duration_seconds")
    private Integer totalDurationSeconds;

    @Column(name = "total_tables") 
    private Integer totalTables;

    @Column(name = "average_occupancy_rate")
    private Double averageOccupancyRate;


    @OneToMany(
        mappedBy = "analysisTask",
        cascade = CascadeType.ALL,
        orphanRemoval = true,
        fetch = FetchType.LAZY
    )
    @Builder.Default
    private List<TableZone> tableZones = new ArrayList<>();

    @OneToMany(
        mappedBy = "analysisTask",
        cascade = CascadeType.ALL,
        orphanRemoval = true,
        fetch = FetchType.LAZY
    )
    @Builder.Default
    private List<OccupancyPeriod> periods = new ArrayList<>();

    @PrePersist
    protected void onCreate() {
        if (createdAt == null)
            createdAt = LocalDateTime.now();
        if (status == null)
            status = "CREATED";
    }

    // Utility methods
    public void addTableZone(TableZone zone) {
        tableZones.add(zone);
        zone.setAnalysisTask(this);
    }

    public void removeTableZone(TableZone zone) {
        tableZones.remove(zone);
        zone.setAnalysisTask(this);
    }

    public void addPeriod(OccupancyPeriod period) {
        periods.add(period);
        period.setAnalysisTask(this);
    }

    public void removePeriod(OccupancyPeriod period) {
        periods.remove(period);
        period.setAnalysisTask(this);
    }
}

