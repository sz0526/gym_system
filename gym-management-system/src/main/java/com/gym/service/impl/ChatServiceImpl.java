package com.gym.service.impl;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.gym.service.ChatService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

@Service
public class ChatServiceImpl implements ChatService {

    @Value("${rag.api.url}")
    private String ragUrl;

    private final ObjectMapper mapper = new ObjectMapper();

    @Override
    public String queryChat(String content, String model) {
        try {
            Map<String, String> body = new HashMap<>();
            body.put("question", content);

            String json = mapper.writeValueAsString(body);

            HttpURLConnection conn =
                    (HttpURLConnection) new URL(ragUrl + "/chat").openConnection();
            conn.setRequestMethod("POST");
            conn.setDoOutput(true);
            conn.setRequestProperty("Content-Type", "application/json;charset=UTF-8");

            try (OutputStream os = conn.getOutputStream()) {
                os.write(json.getBytes(StandardCharsets.UTF_8));
            }

            String result = readAll(conn.getInputStream());
            JsonNode root = mapper.readTree(result);
            return root.get("answer").asText();

        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public SseEmitter streamChat(String content) {
        SseEmitter emitter = new SseEmitter(0L);

        CompletableFuture.runAsync(() -> {
            try {
                Map<String, String> body = new HashMap<>();
                body.put("question", content);
                String json = mapper.writeValueAsString(body);

                HttpURLConnection conn =
                        (HttpURLConnection) new URL(ragUrl + "/chat/stream").openConnection();
                conn.setRequestMethod("POST");
                conn.setDoOutput(true);
                conn.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
                conn.setRequestProperty("Accept-Charset", "UTF-8");

                try (OutputStream os = conn.getOutputStream()) {
                    os.write(json.getBytes(StandardCharsets.UTF_8));
                }

                BufferedReader reader = new BufferedReader(
                        new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8));

                org.springframework.http.MediaType utf8Text =
                        org.springframework.http.MediaType.parseMediaType("text/plain;charset=UTF-8");

                String line;
                while ((line = reader.readLine()) != null) {
                    if (line.startsWith("data:")) {
                        line = line.substring(5).trim();
                    }
                    if (!line.isEmpty()) {
                        emitter.send(SseEmitter.event().data(line, utf8Text));
                    }
                }
                reader.close();
                emitter.complete();

            } catch (Exception e) {
                emitter.completeWithError(e);
            }
        });

        return emitter;
    }

    private String readAll(InputStream is) throws Exception {
        StringBuilder sb = new StringBuilder();
        BufferedReader br = new BufferedReader(
                new InputStreamReader(is, StandardCharsets.UTF_8));
        String line;
        while ((line = br.readLine()) != null) {
            sb.append(line);
        }
        br.close();
        return sb.toString();
    }
}