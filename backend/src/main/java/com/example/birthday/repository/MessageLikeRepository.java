package com.example.birthday.repository;

import com.example.birthday.domain.MessageLike;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MessageLikeRepository extends JpaRepository<MessageLike, Long> {

    boolean existsByMessageIdAndVisitorId(Long messageId, String visitorId);
}
