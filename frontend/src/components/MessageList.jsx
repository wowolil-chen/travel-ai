import {
  useEffect,
  useRef,
} from "react";

import {
  List,
  Typography,
} from "antd";

const { Text } = Typography;

function MessageList({
  messages,
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  return (
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
          emptyText: "开始聊天吧",
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

      <div ref={bottomRef} />
    </div>
  );
}

export default MessageList;