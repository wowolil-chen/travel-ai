import request from "./request";

/**
 * AI 聊天
 */
export function chat(data) {
  return request.post("/chat", data);
}