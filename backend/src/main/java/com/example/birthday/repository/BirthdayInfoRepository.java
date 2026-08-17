package com.example.birthday.repository;

import com.example.birthday.domain.BirthdayInfo;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface BirthdayInfoRepository extends JpaRepository<BirthdayInfo, Long> {

    Optional<BirthdayInfo> findFirstByOrderByIdAsc();
}
