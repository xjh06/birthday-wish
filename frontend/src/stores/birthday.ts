import { defineStore } from "pinia";
import {
  FALLBACK_BIRTHDAY_INFO,
  FALLBACK_MESSAGES,
} from "../config/site";
import type {
  BirthdayInfo,
  BirthdayMessage,
  BirthdayStats,
  CreateMessagePayload,
} from "../types";
import {
  getBirthdayInfo,
  getMessages,
  getStats,
  likeMessage as likeMessageApi,
  submitMessage as submitMessageApi,
} from "../api";

function getOrCreateVisitorId() {
  let visitorId = localStorage.getItem("birthday-visitor-id");
  if (!visitorId) {
    const randomPart =
      globalThis.crypto?.randomUUID?.() ??
      `${Date.now()}-${Math.random().toString(16).slice(2)}`;
    visitorId = randomPart;
    localStorage.setItem("birthday-visitor-id", visitorId);
  }
  return visitorId;
}

function loadLocalMessages(): BirthdayMessage[] {
  const saved = localStorage.getItem("birthday-local-messages");
  if (saved) {
    try {
      return JSON.parse(saved) as BirthdayMessage[];
    } catch {
      return FALLBACK_MESSAGES;
    }
  }
  return FALLBACK_MESSAGES;
}

export const useBirthdayStore = defineStore("birthday", {
  state: () => ({
    visitorId: getOrCreateVisitorId(),
    info: FALLBACK_BIRTHDAY_INFO as BirthdayInfo,
    messages: loadLocalMessages() as BirthdayMessage[],
    stats: {
      visitCount: 0,
      messageCount: 0,
      totalLikes: 0,
    } as BirthdayStats,
    apiOnline: false,
    initializing: false,
    submitting: false,
  }),
  actions: {
    async initialize() {
      this.initializing = true;
      try {
        const [info, messagePage, stats] = await Promise.all([
          getBirthdayInfo(),
          getMessages(),
          getStats(),
        ]);
        this.info = info;
        this.messages = messagePage.content;
        this.stats = stats;
        this.apiOnline = true;
      } catch {
        this.apiOnline = false;
      } finally {
        this.initializing = false;
      }
    },
    async submitMessage(payload: CreateMessagePayload) {
      this.submitting = true;
      try {
        if (this.apiOnline) {
          const created = await submitMessageApi(payload);
          this.messages.unshift(created);
          this.stats.messageCount += 1;
        } else {
          const localMessage: BirthdayMessage = {
            id: `local-${Date.now()}`,
            senderName: payload.senderName,
            relationship: payload.relationship,
            content: payload.content,
            likeCount: 0,
            createdAt: new Date().toISOString(),
            visible: true,
          };
          this.messages.unshift(localMessage);
          this.stats.messageCount += 1;
          localStorage.setItem("birthday-local-messages", JSON.stringify(this.messages));
        }
        return true;
      } catch (error) {
        console.error("留言提交失败", error);
        return false;
      } finally {
        this.submitting = false;
      }
    },
    async toggleLike(message: BirthdayMessage) {
      const current = this.messages.find((item) => item.id === message.id);
      if (!current) return;

      if (this.apiOnline) {
        try {
          const updated = await likeMessageApi(message.id);
          current.likeCount = updated.likeCount;
          this.stats.totalLikes = this.messages.reduce((sum, item) => sum + item.likeCount, 0);
        } catch {
          // 重复点赞或网络异常时不改变 UI，交由表单提示层处理。
        }
      } else {
        current.likeCount += 1;
        this.stats.totalLikes += 1;
        localStorage.setItem("birthday-local-messages", JSON.stringify(this.messages));
      }
    },
  },
});
