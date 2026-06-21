package com.gym.service;

import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

public interface ChatService {

    /**
     * 普通聊天
     */
    String queryChat(String content, String model);

    /**
     * 流式聊天
     */
    SseEmitter streamChat(String message);

}