import axios from "axios";
import type {
  ApiResponse,
  BirthdayInfo,
  BirthdayMessage,
  BirthdayStats,
  CreateMessagePayload,
  PageResult,
} from "../types";

const baseURL = import.meta.env.VITE_API_BASE_URL || "/api";

export const apiClient = axios.create({
  baseURL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  const visitorId = localStorage.getItem("birthday-visitor-id");
  if (visitorId) {
    config.headers.set("X-Visitor-Id", visitorId);
  }
  return config;
});

export async function getBirthdayInfo() {
  const { data } = await apiClient.get<ApiResponse<BirthdayInfo>>("/birthday/info");
  return data.data;
}

export async function getMessages(page = 0, size = 30) {
  const { data } = await apiClient.get<ApiResponse<PageResult<BirthdayMessage>>>("/messages", {
    params: { page, size },
  });
  return data.data;
}

export async function submitMessage(payload: CreateMessagePayload) {
  const { data } = await apiClient.post<ApiResponse<BirthdayMessage>>("/messages", payload);
  return data.data;
}

export async function likeMessage(messageId: number | string) {
  const { data } = await apiClient.post<ApiResponse<BirthdayMessage>>(`/messages/${messageId}/like`);
  return data.data;
}

export async function getStats() {
  const { data } = await apiClient.get<ApiResponse<BirthdayStats>>("/stats");
  return data.data;
}
