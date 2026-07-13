import { useState } from "react";

import {
  Button,
  Input,
} from "antd";

import { SendOutlined } from "@ant-design/icons";

const { TextArea } = Input;

function ChatInput({
  loading,
  onSend,
  isMobile,
}) {
  const [input, setInput] =
    useState("");

  const handleSend = () => {
    if (!input.trim()) return;

    onSend(input);

    setInput("");
  };

  const handleKeyDown = (e) => {
    if (
      e.key === "Enter" &&
      !e.shiftKey
    ) {
      e.preventDefault();

      handleSend();
    }
  };

  return (
    <div
      style={{
        display: "flex",
        gap: isMobile ? 8 : 12,
        marginTop: isMobile ? 12 : 20,
      }}
    >
      <TextArea
        rows={isMobile ? 2 : 3}
        value={input}
        placeholder="请输入旅游需求..."
        onChange={(e) =>
          setInput(e.target.value)
        }
        onKeyDown={handleKeyDown}
        style={{
          fontSize: isMobile ? 14 : 15,
        }}
      />

      <Button
        type="primary"
        loading={loading}
        icon={<SendOutlined />}
        onClick={handleSend}
        style={{
          height: "auto",
          fontSize: isMobile ? 14 : 15,
          padding: isMobile ? "8px 12px" : "12px 16px",
        }}
      >
        {isMobile ? "" : "发送"}
      </Button>
    </div>
  );
}

export default ChatInput;