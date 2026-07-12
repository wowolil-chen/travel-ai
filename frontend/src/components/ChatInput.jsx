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
        gap: 12,
        marginTop: 20,
      }}
    >
      <TextArea
        rows={3}
        value={input}
        placeholder="请输入旅游需求..."
        onChange={(e) =>
          setInput(e.target.value)
        }
        onKeyDown={handleKeyDown}
      />

      <Button
        type="primary"
        loading={loading}
        icon={<SendOutlined />}
        onClick={handleSend}
        style={{
          height: "auto",
        }}
      >
        发送
      </Button>
    </div>
  );
}

export default ChatInput;