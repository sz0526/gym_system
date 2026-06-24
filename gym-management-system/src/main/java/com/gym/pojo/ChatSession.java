package com.gym.pojo;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class ChatSession {

    private Long id;

    private String memberAccount;

    private String title;

    private LocalDateTime createTime;
}