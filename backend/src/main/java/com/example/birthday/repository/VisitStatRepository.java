package com.example.birthday.repository;

import com.example.birthday.domain.VisitStat;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.time.LocalDate;
import java.util.Optional;

public interface VisitStatRepository extends JpaRepository<VisitStat, Long> {

    Optional<VisitStat> findByVisitDate(LocalDate visitDate);

    @Query("select coalesce(sum(v.visitCount), 0) from VisitStat v")
    long sumVisitCounts();
}
