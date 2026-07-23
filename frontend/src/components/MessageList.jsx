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
  isMobile,
  loading,
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
        paddingRight: isMobile ? 5 : 10,
      }}
    >
      <List
        dataSource={messages}
        locale={{
          emptyText: "开始聊天吧",
        }}
        renderItem={(item, index) => (
          <List.Item
            style={{
              border: "none",
              display: "flex",
              justifyContent:
                item.role === "user"
                  ? "flex-end"
                  : "flex-start",
              padding: isMobile ? "8px 0" : "12px 0",
            }}
          >
            {(() => {
              const isThinking =
                loading &&
                index === messages.length - 1 &&
                item.role === "assistant" &&
                !item.content;

              const content = isThinking
                ? "AI正在玩命思考中，请稍等..."
                : item.content;

              return (
            <div
              style={{
                maxWidth: isMobile ? "85%" : "70%",
                background:
                  item.role === "user"
                    ? "#1677ff"
                    : "#ffffff",
                color:
                  item.role === "user"
                    ? "#ffffff"
                    : "#000000",
                padding: isMobile ? "10px 14px" : "12px 16px",
                borderRadius: 12,
                boxShadow:
                  "0 2px 8px rgba(0,0,0,.08)",
                whiteSpace: "pre-wrap",
                fontSize: isMobile ? 14 : 15,
                lineHeight: 1.5,
              }}
            >
              <Text
                style={{
                  color:
                    item.role === "user"
                      ? "#ffffff"
                      : isThinking
                        ? "rgba(0,0,0,.45)"
                        : "#000000",
                  fontStyle:
                    isThinking ? "italic" : "normal",
                }}
              >
                {content}
              </Text>
            </div>
              );
            })()}
          </List.Item>
        )}
      />

      <div ref={bottomRef} />
    </div>
  );
}

export default MessageList;
