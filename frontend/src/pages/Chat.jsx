import { useState } from "react";

import ChatLayout from "../layouts/ChatLayout";

import Sidebar from "../components/Sidebar";
import ChatHeader from "../components/ChatHeader";
import MessageList from "../components/MessageList";
import ChatInput from "../components/ChatInput";

function Chat() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "你好，我是 Travel AI，请问有什么可以帮助你的？",
    },
  ]);

  const [loading, setLoading] = useState(false);

  return (
    <ChatLayout
      sidebar={<Sidebar />}
      content={
        <div
          style={{
            height: "100vh",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <ChatHeader />

          <MessageList
            messages={messages}
            loading={loading}
          />

          <ChatInput
            setMessages={setMessages}
            loading={loading}
            setLoading={setLoading}
          />
        </div>
      }
    />
  );
}

export default Chat;