package com.gym.mapper;

import com.gym.pojo.ChatMessage;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface ChatMessageMapper {

    /**
     * 保存消息
     */
    int insert(ChatMessage message);

    /**
     * 查询最近N条消息
     */
    List<ChatMessage> selectLastMessages(
            @Param("sessionId") Long sessionId,
            @Param("limit") Integer limit
    );

}