import request from "./request";

/**
 * 创建会话
 */
export function createConversation(title = "新对话") {
    return request.post("/conversations", {
        title,
    });
}

/**
 * 获取会话列表
 */
export function getConversationList() {
    return request.get("/conversations");
}

/**
 * 删除会话
 */
export function deleteConversation(conversationId) {
    return request.delete(`/conversations/${conversationId}`);
}

/**
 * 获取消息记录（后面会用）
 */
export function getMessages(conversationId) {
    return request.get(`/conversations/${conversationId}/messages`);
}

/**
 * 流式聊天
 */
export async function streamChat(
    conversationId,
    message,
    onMessage,
    onFinish,
    onError,
) {
    const token = localStorage.getItem("token");

    try {

        const response = await fetch(
            "http://localhost:8001/api/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },

                body: JSON.stringify({
                    conversation_id: conversationId,
                    message,
                }),
            },
        );

        if (!response.ok) {
            throw new Error("聊天失败");
        }

        const reader = response.body.getReader();

        const decoder = new TextDecoder("utf-8");

        let result = "";

        while (true) {

            const { done, value } = await reader.read();

            if (done) break;

            const chunk = decoder.decode(value);

            result += chunk;

            onMessage(result);
        }

        onFinish(result);

    } catch (error) {

        if (onError) {
            onError(error);
        }

    }

}