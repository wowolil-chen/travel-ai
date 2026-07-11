import { useEffect, useRef, useState } from "react";
import { Button, Input, Layout, List, message, Spin, Typography } from "antd";
import { SendOutlined } from "@ant-design/icons";
import { chat } from "../api/chat";

const { Content } = Layout;
const { Text } = Typography;
const { TextArea } = Input;

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const messageEndRef = useRef(null);

  // 自动滚动到底部
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  // 发送消息
  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const question = input.trim();

    const userMessage = {
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    setInput("");
    setLoading(true);

    try {
      const res = await chat(question);

      const aiMessage = {
        role: "assistant",
        content: res.reply,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error(error);

      message.error("AI 回复失败");
    } finally {
      setLoading(false);
    }
  };

  // Enter发送 Shift+Enter换行
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Layout style={{ height: "100%" }}>
      <Content
        style={{
          display: "flex",
          flexDirection: "column",
          padding: 20,
          background: "#f5f5f5",
        }}
      >
        {/* 聊天区域 */}
        <div
          style={{
            flex: 1,
            overflowY: "auto",
            paddingRight: 10,
          }}
        >
          <List
            dataSource={messages}
            locale={{
              emptyText: "开始和 AI 聊天吧～",
            }}
            renderItem={(item) => (
              <List.Item
                style={{
                  border: "none",
                  display: "flex",
                  justifyContent:
                    item.role === "user"
                      ? "flex-end"
                      : "flex-start",
                }}
              >
                <div
                  style={{
                    maxWidth: "70%",
                    background:
                      item.role === "user"
                        ? "#1677ff"
                        : "#ffffff",
                    color:
                      item.role === "user"
                        ? "#ffffff"
                        : "#000000",
                    padding: "12px 16px",
                    borderRadius: 12,
                    boxShadow:
                      "0 2px 8px rgba(0,0,0,.08)",
                    whiteSpace: "pre-wrap",
                  }}
                >
                  <Text
                    style={{
                      color:
                        item.role === "user"
                          ? "#ffffff"
                          : "#000000",
                    }}
                  >
                    {item.content}
                  </Text>
                </div>
              </List.Item>
            )}
          />

          {loading && (
            <div
              style={{
                display: "flex",
                marginTop: 10,
              }}
            >
              <Spin />
            </div>
          )}

          <div ref={messageEndRef} />
        </div>

        {/* 输入区域 */}
        <div
          style={{
            marginTop: 20,
            display: "flex",
            gap: 12,
          }}
        >
          <TextArea
            value={input}
            rows={3}
            placeholder="请输入你的旅行需求..."
            onChange={(e) =>
              setInput(e.target.value)
            }
            onKeyDown={handleKeyDown}
          />

          <Button
            type="primary"
            icon={<SendOutlined />}
            loading={loading}
            onClick={handleSend}
            style={{
              height: "auto",
            }}
          >
            发送
          </Button>
        </div>
      </Content>
    </Layout>
  );
}