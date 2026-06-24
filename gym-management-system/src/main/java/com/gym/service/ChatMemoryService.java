package com.gym.service;

import com.gym.pojo.ChatMessage;

import java.util.List;

public interface ChatMemoryService {

    void saveUserMessage(Long sessionId,String content);

    void saveAssistantMessage(Long sessionId,String content);

    List<ChatMessage> getRecentMessages(
            Long sessionId,
            Integer limit
    );
}