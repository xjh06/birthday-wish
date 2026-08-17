package com.example.birthday.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.time.LocalDate;

@Entity
@Table(name = "birthday_info")
public class BirthdayInfo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "recipient_name", nullable = false, length = 80)
    private String recipientName;

    @Column(name = "birthday_date", nullable = false)
    private LocalDate birthdayDate;

    @Column(name = "hero_title", nullable = false, length = 160)
    private String heroTitle;

    @Column(name = "blessing_title", nullable = false, length = 160)
    private String blessingTitle;

    @Column(name = "blessing_text", nullable = false, length = 1000)
    private String blessingText;

    @Column(name = "card_salutation", nullable = false, length = 80)
    private String cardSalutation;

    @Column(name = "card_message", nullable = false, length = 1000)
    private String cardMessage;

    @Column(name = "music_url", length = 1000)
    private String musicUrl;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getRecipientName() {
        return recipientName;
    }

    public void setRecipientName(String recipientName) {
        this.recipientName = recipientName;
    }

    public LocalDate getBirthdayDate() {
        return birthdayDate;
    }

    public void setBirthdayDate(LocalDate birthdayDate) {
        this.birthdayDate = birthdayDate;
    }

    public String getHeroTitle() {
        return heroTitle;
    }

    public void setHeroTitle(String heroTitle) {
        this.heroTitle = heroTitle;
    }

    public String getBlessingTitle() {
        return blessingTitle;
    }

    public void setBlessingTitle(String blessingTitle) {
        this.blessingTitle = blessingTitle;
    }

    public String getBlessingText() {
        return blessingText;
    }

    public void setBlessingText(String blessingText) {
        this.blessingText = blessingText;
    }

    public String getCardSalutation() {
        return cardSalutation;
    }

    public void setCardSalutation(String cardSalutation) {
        this.cardSalutation = cardSalutation;
    }

    public String getCardMessage() {
        return cardMessage;
    }

    public void setCardMessage(String cardMessage) {
        this.cardMessage = cardMessage;
    }

    public String getMusicUrl() {
        return musicUrl;
    }

    public void setMusicUrl(String musicUrl) {
        this.musicUrl = musicUrl;
    }
}
