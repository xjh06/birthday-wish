package com.example.birthday.config;

import com.example.birthday.domain.BirthdayInfo;
import com.example.birthday.repository.BirthdayInfoRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import java.time.LocalDate;

@Component
@Profile("postgres")
public class DataInitializer implements CommandLineRunner {

    private final BirthdayInfoRepository birthdayInfoRepository;

    public DataInitializer(BirthdayInfoRepository birthdayInfoRepository) {
        this.birthdayInfoRepository = birthdayInfoRepository;
    }

    @Override
    public void run(String... args) {
        if (birthdayInfoRepository.findFirstByOrderByIdAsc().isPresent()) {
            return;
        }

        BirthdayInfo info = new BirthdayInfo();
        info.setRecipientName("廖思覃");
        info.setBirthdayDate(LocalDate.of(2026, 8, 17));
        info.setHeroTitle("廖思覃，生日快乐");
        info.setBlessingTitle("给新一岁的你");
        info.setBlessingText("愿你的每一天，都有微小的惊喜在等着你。");
        info.setCardSalutation("亲爱的廖思覃");
        info.setCardMessage("叮！按时长大！愿你新的一岁暴富暴美，快乐加倍！");
        info.setMusicUrl("/Christina Perri - A Thousand Years.mp3");
        birthdayInfoRepository.save(info);
    }
}
