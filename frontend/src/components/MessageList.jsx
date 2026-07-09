import { useEffect, useRef } from "react";

function MessageList({ messages, loading }) {
  const bottomRef = useRef(null);

  // 每次消息变化后自动滚动到底部
  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  return (
    <div
      style={{
        flex: 1,
        padding: 24,
        overflowY: "auto",
        background: "#f5f5f5",
      }}
    >
      {messages.map((item, index) => (
        <div
          key={index}
          style={{
            display: "flex",
            justifyContent:
              item.role === "user"
                ? "flex-end"
                : "flex-start",
            marginBottom: 20,
          }}
        >
          <div
            style={{
              maxWidth: "70%",
              padding: "12px 16px",
              borderRadius: 12,
              background:
                item.role === "user"
                  ? "#1677ff"
                  : "#ffffff",
              color:
                item.role === "user"
                  ? "#ffffff"
                  : "#000000",
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
            }}
          >
            {item.content}
          </div>
        </div>
      ))}

      {loading && (
        <div
          style={{
            display: "flex",
            justifyContent: "flex-start",
            marginBottom: 20,
          }}
        >
          <div
            style={{
              padding: "12px 16px",
              borderRadius: 12,
              background: "#ffffff",
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
            }}
          >
            🤖 AI 正在思考...
          </div>
        </div>
      )}

      {/* 自动滚动锚点 */}
      <div ref={bottomRef}></div>
    </div>
  );
}

export default MessageList;