package com.example.birthday.dto;

import com.example.birthday.domain.BirthdayMessage;

import java.time.LocalDateTime;

public record BirthdayMessageResponse(
    Long id,
    String senderName,
    String relationship,
    String content,
    int likeCount,
    LocalDateTime createdAt,
    boolean visible
) {

    public static BirthdayMessageResponse from(BirthdayMessage message) {
        return new BirthdayMessageResponse(
            message.getId(),
            message.getSenderName(),
            message.getRelationship(),
            message.getContent(),
            message.getLikeCount(),
            message.getCreatedAt(),
            message.isVisible()
        );
    }
}
