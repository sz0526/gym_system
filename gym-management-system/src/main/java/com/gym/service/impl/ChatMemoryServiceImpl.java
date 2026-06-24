package com.gym.service.impl;

import com.gym.mapper.ChatMessageMapper;
import com.gym.pojo.ChatMessage;
import com.gym.service.ChatMemoryService;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ChatMemoryServiceImpl
        implements ChatMemoryService {

    private final ChatMessageMapper mapper;

    public ChatMemoryServiceImpl(
            ChatMessageMapper mapper
    ) {
        this.mapper = mapper;
    }

    @Override
    public void saveUserMessage(
            Long sessionId,
            String content
    ) {

        ChatMessage msg = new ChatMessage();

        msg.setSessionId(sessionId);
        msg.setRole("user");
        msg.setContent(content);

        mapper.insert(msg);
    }

    @Override
    public void saveAssistantMessage(
            Long sessionId,
            String content
    ) {

        ChatMessage msg = new ChatMessage();

        msg.setSessionId(sessionId);
        msg.setRole("assistant");
        msg.setContent(content);

        mapper.insert(msg);
    }

    @Override
    public List<ChatMessage> getRecentMessages(
            Long sessionId,
            Integer limit
    ) {
        return mapper.selectLastMessages(
                sessionId,
                limit
        );
    }
}