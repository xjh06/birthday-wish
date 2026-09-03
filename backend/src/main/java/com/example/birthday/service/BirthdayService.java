package com.example.birthday.service;

import com.example.birthday.common.BusinessException;
import com.example.birthday.domain.BirthdayInfo;
import com.example.birthday.domain.BirthdayMessage;
import com.example.birthday.domain.MessageLike;
import com.example.birthday.domain.VisitStat;
import com.example.birthday.dto.BirthdayInfoResponse;
import com.example.birthday.dto.BirthdayMessageResponse;
import com.example.birthday.dto.CreateMessageRequest;
import com.example.birthday.dto.PageResponse;
import com.example.birthday.dto.StatsResponse;
import com.example.birthday.repository.BirthdayInfoRepository;
import com.example.birthday.repository.BirthdayMessageRepository;
import com.example.birthday.repository.MessageLikeRepository;
import com.example.birthday.repository.VisitStatRepository;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;

@Service
public class BirthdayService {

    private final BirthdayInfoRepository birthdayInfoRepository;
    private final BirthdayMessageRepository messageRepository;
    private final MessageLikeRepository messageLikeRepository;
    private final VisitStatRepository visitStatRepository;

    public BirthdayService(
        BirthdayInfoRepository birthdayInfoRepository,
        BirthdayMessageRepository messageRepository,
        MessageLikeRepository messageLikeRepository,
        VisitStatRepository visitStatRepository
    ) {
        this.birthdayInfoRepository = birthdayInfoRepository;
        this.messageRepository = messageRepository;
        this.messageLikeRepository = messageLikeRepository;
        this.visitStatRepository = visitStatRepository;
    }

    public BirthdayInfoResponse getBirthdayInfo() {
        BirthdayInfo info = birthdayInfoRepository.findFirstByOrderByIdAsc()
            .orElseThrow(() -> new BusinessException(404, 404, "生日配置尚未初始化"));
        return BirthdayInfoResponse.from(info);
    }

    public PageResponse<BirthdayMessageResponse> getMessages(int page, int size) {
        int safePage = Math.max(page, 0);
        int safeSize = Math.min(Math.max(size, 1), 50);
        Page<BirthdayMessage> messages = messageRepository.findByVisibleTrueOrderByCreatedAtDesc(
            PageRequest.of(safePage, safeSize)
        );
        return new PageResponse<>(
            messages.getContent().stream().map(BirthdayMessageResponse::from).toList(),
            messages.getNumber(),
            messages.getSize(),
            messages.getTotalElements(),
            messages.getTotalPages()
        );
    }

    @Transactional
    public BirthdayMessageResponse createMessage(CreateMessageRequest request) {
        BirthdayMessage message = new BirthdayMessage();
        message.setSenderName(clean(request.senderName()));
        message.setRelationship(cleanBlank(request.relationship(), "朋友"));
        message.setContent(clean(request.content()));
        message.setLikeCount(0);
        message.setVisible(true);
        return BirthdayMessageResponse.from(messageRepository.save(message));
    }

    @Transactional
    public BirthdayMessageResponse likeMessage(Long messageId, String visitorId) {
        if (visitorId == null || visitorId.isBlank()) {
            throw new BusinessException(400, 400, "缺少访客标识");
        }

        BirthdayMessage message = messageRepository.findById(messageId)
            .orElseThrow(() -> new BusinessException(404, 404, "留言不存在"));

        if (messageLikeRepository.existsByMessageIdAndVisitorId(messageId, visitorId)) {
            throw new BusinessException(409, 409, "你已经点过赞啦");
        }

        try {
            messageLikeRepository.save(new MessageLike(messageId, visitorId));
        } catch (DataIntegrityViolationException e) {
            // 并发点赞时，数据库唯一约束（message_id + visitor_id）会拒绝第二条记录，
            // 统一转换为 409，避免向客户端返回 500。
            throw new BusinessException(409, 409, "你已经点过赞啦");
        }
        message.setLikeCount(message.getLikeCount() + 1);
        return BirthdayMessageResponse.from(messageRepository.save(message));
    }

    @Transactional
    public StatsResponse getStats() {
        LocalDate today = LocalDate.now();
        VisitStat stat = visitStatRepository.findByVisitDate(today).orElseGet(() -> {
            VisitStat created = new VisitStat(today);
            created.setVisitCount(0);
            return created;
        });
        stat.setVisitCount(stat.getVisitCount() + 1);
        visitStatRepository.save(stat);

        long visitCount = visitStatRepository.sumVisitCounts();
        long messageCount = messageRepository.countByVisibleTrue();
        long totalLikes = messageRepository.sumLikeCounts();
        return new StatsResponse(visitCount, messageCount, totalLikes);
    }

    private String clean(String value) {
        return value == null ? "" : value.replaceAll("[\\p{Cntrl}]", "").trim();
    }

    private String cleanBlank(String value, String fallback) {
        String cleaned = clean(value);
        return cleaned.isBlank() ? fallback : cleaned;
    }
}
