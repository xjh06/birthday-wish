package com.example.birthday.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record CreateMessageRequest(
    @NotBlank(message = "请填写你的名字")
    @Size(min = 2, max = 30, message = "名字长度需要在 2 到 30 字之间")
    String senderName,

    @Size(max = 30, message = "关系长度不能超过 30 字")
    String relationship,

    @NotBlank(message = "请填写祝福内容")
    @Size(min = 2, max = 500, message = "祝福内容需要在 2 到 500 字之间")
    String content
) {
}
