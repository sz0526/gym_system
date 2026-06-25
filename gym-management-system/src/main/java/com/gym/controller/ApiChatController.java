package com.gym.controller;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.gym.pojo.ClassOrder;
import com.gym.pojo.Member;
import com.gym.service.ChatMemoryService;
import com.gym.service.ChatService;
import com.gym.service.ClassOrderService;
import com.gym.service.MemberService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/chat")
public class ApiChatController {

    @Autowired
    private ChatService chatService;

    @Autowired
    private ClassOrderService classOrderService;

    @Autowired
    private ChatMemoryService chatMemoryService;

    @Autowired
    private MemberService memberService;

    @Value("${rag.api.url}")
    private String ragUrl;

    private final ObjectMapper objectMapper = new ObjectMapper();

    // 创建 RAG 会话
    @PostMapping("/session/create")
    public Map<String, Object> createRagSession() {
        Map<String, Object> resp = new HashMap<>();
        try {
            HttpURLConnection conn =
                    (HttpURLConnection) new URL(ragUrl + "/session/create").openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
            conn.setDoOutput(true);
            conn.getOutputStream().write("{}".getBytes(StandardCharsets.UTF_8));

            String result = new BufferedReader(
                    new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8))
                    .lines().collect(Collectors.joining());

            JsonNode node = objectMapper.readTree(result);
            resp.put("success", true);
            resp.put("sessionId", node.get("session_id").asText());
        } catch (Exception e) {
            resp.put("success", false);
            resp.put("message", e.getMessage());
        }
        return resp;
    }

    @PostMapping("/query")
    public Map<String, Object> query(
            @RequestParam("content") String content,
            @RequestParam(required = false) String model,
            HttpSession session
    ) {
        HashMap<String, Object> resp = new HashMap<>();
        try {
            Member member = (Member) session.getAttribute("user");
            String enhancedContent = buildContentWithMemberClasses(content, member);

            Long sessionId = 1L;
            chatMemoryService.saveUserMessage(sessionId, content);

            String reply = chatService.queryChat(enhancedContent, model);
            chatMemoryService.saveAssistantMessage(sessionId, reply);

            resp.put("success", true);
            resp.put("reply", reply);
        } catch (Exception e) {
            resp.put("success", false);
            resp.put("message", e.getMessage());
        }
        return resp;
    }

    @GetMapping(value = "/stream", produces = "text/event-stream;charset=UTF-8")
    public SseEmitter stream(
            @RequestParam("content") String content,
            @RequestParam(required = false) String memberAccount,
            @RequestParam(required = false) String ragSessionId,
            HttpSession session
    ) {
        // 获取用户信息
        Member member = (Member) session.getAttribute("user");
        if (member == null && memberAccount != null) {
            try {
                List<Member> members = memberService.selectByMemberAccount(Integer.parseInt(memberAccount));
                if (members != null && !members.isEmpty()) {
                    member = members.get(0);
                }
            } catch (NumberFormatException e) {
                // 忽略
            }
        }

        Long sessionId = 1L;

        // 存用户消息
        chatMemoryService.saveUserMessage(sessionId, content);

        // 拼课程上下文
        final String finalContent = buildContentWithMemberClasses(content, member);
        final String finalRagSessionId = (ragSessionId != null && !ragSessionId.isEmpty())
                ? ragSessionId : "default";

        SseEmitter emitter = new SseEmitter(0L);

        CompletableFuture.runAsync(() -> {
            try {
                Map<String, Object> body = new HashMap<>();
                body.put("question", finalContent);
                body.put("session_id", finalRagSessionId);
                body.put("n_rounds", 5);
                String json = objectMapper.writeValueAsString(body);

                HttpURLConnection conn =
                        (HttpURLConnection) new URL(ragUrl + "/chat/session/stream").openConnection();
                conn.setRequestMethod("POST");
                conn.setDoOutput(true);
                conn.setRequestProperty("Content-Type", "application/json;charset=UTF-8");

                try (OutputStream os = conn.getOutputStream()) {
                    os.write(json.getBytes(StandardCharsets.UTF_8));
                }

                BufferedReader reader = new BufferedReader(
                        new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8));

                MediaType utf8Text = MediaType.parseMediaType("text/plain;charset=UTF-8");
                StringBuilder fullReply = new StringBuilder();

                String line;
                while ((line = reader.readLine()) != null) {
                    if (line.startsWith("data:")) {
                        line = line.substring(5).trim();
                    }
                    if (!line.isEmpty()) {
                        fullReply.append(line);
                        emitter.send(SseEmitter.event().data(line, utf8Text));
                    }
                }
                reader.close();

                // 存 AI 回复
                chatMemoryService.saveAssistantMessage(sessionId, fullReply.toString());
                emitter.complete();

            } catch (Exception e) {
                emitter.completeWithError(e);
            }
        });

        return emitter;
    }

    @GetMapping(value = "/agent/stream", produces = "text/event-stream;charset=UTF-8")
    public SseEmitter agentStream(
            @RequestParam("content") String content,
            @RequestParam(required = false) String memberAccount,
            HttpSession session
    ) {
        Member member = (Member) session.getAttribute("user");
        if (member == null && memberAccount != null) {
            try {
                List<Member> members = memberService.selectByMemberAccount(Integer.parseInt(memberAccount));
                if (members != null && !members.isEmpty()) {
                    member = members.get(0);
                }
            } catch (NumberFormatException e) {
                // 忽略
            }
        }

        Long sessionId = 1L;
        chatMemoryService.saveUserMessage(sessionId, content);

        final String finalMemberAccount = (member != null && member.getMemberAccount() != null)
                ? member.getMemberAccount().toString() : "";
        final String finalContent = content;

        SseEmitter emitter = new SseEmitter(0L);

        CompletableFuture.runAsync(() -> {
            try {
                Map<String, Object> body = new HashMap<>();
                body.put("question", finalContent);
                body.put("member_account", finalMemberAccount);
                String json = objectMapper.writeValueAsString(body);

                HttpURLConnection conn =
                        (HttpURLConnection) new URL(ragUrl + "/agent/chat").openConnection();
                conn.setRequestMethod("POST");
                conn.setDoOutput(true);
                conn.setRequestProperty("Content-Type", "application/json;charset=UTF-8");

                try (OutputStream os = conn.getOutputStream()) {
                    os.write(json.getBytes(StandardCharsets.UTF_8));
                }

                // 读取普通 JSON 回复
                String result = new BufferedReader(
                        new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8))
                        .lines().collect(Collectors.joining());

                JsonNode node = objectMapper.readTree(result);
                String answer = node.get("answer").asText();

                // 模拟流式输出，按字符发送
                MediaType utf8Text = MediaType.parseMediaType("text/plain;charset=UTF-8");
                for (String chunk : answer.split("(?<=\\G.{5})")) {
                    emitter.send(SseEmitter.event().data(chunk, utf8Text));
                    Thread.sleep(30);
                }

                chatMemoryService.saveAssistantMessage(sessionId, answer);
                emitter.complete();

            } catch (Exception e) {
                emitter.completeWithError(e);
            }
        });

        return emitter;
    }

    private String buildContentWithMemberClasses(String originalContent, Member member) {
        if (member == null || member.getMemberAccount() == null) {
            return originalContent;
        }

        List<ClassOrder> classOrders = classOrderService.selectClassOrderByMemberAccount(member.getMemberAccount());
        if (classOrders == null || classOrders.isEmpty()) {
            return originalContent;
        }

        String classInfo = classOrders.stream()
                .map(order -> String.format(
                        "课程名称：%s,教练：%s,上课时间：%s",
                        order.getClassName(),
                        order.getCoach(),
                        order.getClassBegin()
                ))
                .collect(Collectors.joining(";"));

        String memberInfo = String.format("会员姓名：%s,会员账号：%s",
                member.getMemberName(), member.getMemberAccount());

        StringBuilder sb = new StringBuilder();
        sb.append(originalContent == null ? "" : originalContent.trim());
        sb.append("\n\n");
        sb.append("【系统补充信息】下面是该会员当前已报名的课程信息，请先根据这些信息，明确地告诉用户\"我报名了哪些课程\"，然后再结合课程安排回答后续问题：\n");
        sb.append(memberInfo).append("\n");
        sb.append(classInfo);

        return sb.toString();
    }
}