import { useState } from "react";
import { Button, Input, Space } from "antd";

function ChatInput({ setMessages, loading, setLoading }) {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    const content = message.trim();

    if (!content || loading) {
      return;
    }

    // 添加用户消息
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content,
      },
    ]);

    setMessage("");

    // 开始等待 AI 回复
    setLoading(true);

    // 模拟 AI 回复
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "这是模拟回复，下一步将由 DeepSeek 返回。",
        },
      ]);

      setLoading(false);
    }, 1000);
  };

  return (
    <div
      style={{
        padding: 20,
        borderTop: "1px solid #f0f0f0",
        background: "#ffffff",
      }}
    >
      <Space.Compact
        style={{
          width: "100%",
        }}
      >
        <Input
          value={message}
          placeholder="请输入你的问题..."
          onChange={(e) => setMessage(e.target.value)}
          onPressEnter={handleSend}
          disabled={loading}
        />

        <Button
          type="primary"
          loading={loading}
          disabled={loading}
          onClick={handleSend}
        >
          发送
        </Button>
      </Space.Compact>
    </div>
  );
}

export default ChatInput;