package com.example.birthday;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("h2")
@Transactional
class BirthdayControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void shouldReturnBirthdayInfo() throws Exception {
        mockMvc.perform(get("/api/birthday/info"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code", is(0)))
            .andExpect(jsonPath("$.data.recipientName", is("廖思覃")));
    }

    @Test
    void shouldCreateMessage() throws Exception {
        mockMvc.perform(post("/api/messages")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                    {
                      "senderName": "小林",
                      "relationship": "朋友",
                      "content": "祝你生日快乐，每天开心。"
                    }
                    """))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code", is(0)))
            .andExpect(jsonPath("$.data.senderName", is("小林")));
    }

    @Test
    void shouldRejectTooShortMessage() throws Exception {
        mockMvc.perform(post("/api/messages")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                    {
                      "senderName": "小林",
                      "relationship": "朋友",
                      "content": "好"
                    }
                    """))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.code", is(400)));
    }

    @Test
    void shouldLikeMessageOnce() throws Exception {
        long messageId = createMessageAndReturnId();

        mockMvc.perform(post("/api/messages/{id}/like", messageId)
                .header("X-Visitor-Id", "visitor-test-001"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code", is(0)));

        mockMvc.perform(post("/api/messages/{id}/like", messageId)
                .header("X-Visitor-Id", "visitor-test-001"))
            .andExpect(status().isConflict())
            .andExpect(jsonPath("$.code", is(409)));
    }

    private long createMessageAndReturnId() throws Exception {
        String body = mockMvc.perform(post("/api/messages")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                    {
                      "senderName": "小林",
                      "relationship": "朋友",
                      "content": "祝你生日快乐，每天开心。"
                    }
                    """))
            .andExpect(status().isOk())
            .andReturn()
            .getResponse()
            .getContentAsString();

        JsonNode json = objectMapper.readTree(body);
        return json.path("data").path("id").asLong();
    }
}
