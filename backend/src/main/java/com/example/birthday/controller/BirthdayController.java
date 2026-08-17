package com.example.birthday.controller;

import com.example.birthday.common.ApiResponse;
import com.example.birthday.dto.BirthdayInfoResponse;
import com.example.birthday.dto.BirthdayMessageResponse;
import com.example.birthday.dto.CreateMessageRequest;
import com.example.birthday.dto.PageResponse;
import com.example.birthday.dto.StatsResponse;
import com.example.birthday.service.BirthdayService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class BirthdayController {

    private final BirthdayService birthdayService;

    public BirthdayController(BirthdayService birthdayService) {
        this.birthdayService = birthdayService;
    }

    @GetMapping("/birthday/info")
    public ApiResponse<BirthdayInfoResponse> getBirthdayInfo() {
        return ApiResponse.ok(birthdayService.getBirthdayInfo());
    }

    @GetMapping("/messages")
    public ApiResponse<PageResponse<BirthdayMessageResponse>> getMessages(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "30") int size
    ) {
        return ApiResponse.ok(birthdayService.getMessages(page, size));
    }

    @PostMapping("/messages")
    public ApiResponse<BirthdayMessageResponse> createMessage(
        @Valid @RequestBody CreateMessageRequest request
    ) {
        return ApiResponse.ok(birthdayService.createMessage(request));
    }

    @PostMapping("/messages/{id}/like")
    public ApiResponse<BirthdayMessageResponse> likeMessage(
        @PathVariable Long id,
        @RequestHeader(name = "X-Visitor-Id", required = false) String visitorId
    ) {
        return ApiResponse.ok(birthdayService.likeMessage(id, visitorId));
    }

    @GetMapping("/stats")
    public ApiResponse<StatsResponse> getStats() {
        return ApiResponse.ok(birthdayService.getStats());
    }
}
