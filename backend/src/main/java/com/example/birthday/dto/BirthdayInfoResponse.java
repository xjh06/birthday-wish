package com.example.birthday.dto;

import com.example.birthday.domain.BirthdayInfo;

import java.time.format.DateTimeFormatter;

public record BirthdayInfoResponse(
    String recipientName,
    String birthdayDate,
    String heroTitle,
    String blessingTitle,
    String blessingText,
    String cardSalutation,
    String cardMessage,
    String musicUrl
) {

    private static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("M月d日");

    public static BirthdayInfoResponse from(BirthdayInfo info) {
        return new BirthdayInfoResponse(
            info.getRecipientName(),
            info.getBirthdayDate().format(DATE_FORMATTER),
            info.getHeroTitle(),
            info.getBlessingTitle(),
            info.getBlessingText(),
            info.getCardSalutation(),
            info.getCardMessage(),
            info.getMusicUrl()
        );
    }
}
