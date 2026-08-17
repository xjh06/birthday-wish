package com.example.birthday.repository;

import com.example.birthday.domain.BirthdayMessage;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface BirthdayMessageRepository extends JpaRepository<BirthdayMessage, Long> {

    Page<BirthdayMessage> findByVisibleTrueOrderByCreatedAtDesc(Pageable pageable);

    long countByVisibleTrue();

    @Query("select coalesce(sum(m.likeCount), 0) from BirthdayMessage m where m.visible = true")
    long sumLikeCounts();
}
