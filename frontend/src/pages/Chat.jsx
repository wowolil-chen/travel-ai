import { useEffect, useState } from "react";
import { Layout, message } from "antd";

import Sidebar from "../components/Sidebar";
import ChatHeader from "../components/ChatHeader";
import MessageList from "../components/MessageList";
import ChatInput from "../components/ChatInput";

import {
  streamChat,
  getMessages,
} from "../api/chat";

const { Sider, Content } = Layout;

export default function Chat() {

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const [conversationId, setConversationId] = useState(null);

  /**
   * 切换聊天
   */
  useEffect(() => {

    if (!conversationId) {
      setMessages([]);
      return;
    }

    loadMessages();

  }, [conversationId]);

  /**
   * 加载历史消息
   */
  const loadMessages = async () => {

    try {

      const res = await getMessages(
        conversationId
      );

      setMessages(res.data);

    } catch (e) {

      console.error(e);

      message.error("加载历史消息失败");

    }

  };

  /**
   * 发送消息
   */
  const handleSend = async (question) => {

    if (!conversationId) {

      message.warning("请先创建聊天");

      return;

    }

    if (!question.trim() || loading) return;

    setLoading(true);

    const userMessage = {
      role: "user",
      content: question,
    };

    const aiMessage = {
      role: "assistant",
      content: "",
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
      aiMessage,
    ]);

    await streamChat(

      conversationId,

      question,

      (text) => {

        setMessages((prev) => {

          const list = [...prev];

          list[list.length - 1] = {
            role: "assistant",
            content: text,
          };

          return list;

        });

      },

      () => {

        setLoading(false);

      },

      () => {

        setLoading(false);

        message.error("聊天失败");

      }

    );

  };

  return (

    <Layout
      style={{
        height: "100vh",
      }}
    >

      <Sider
        width={280}
        theme="light"
      >

        <Sidebar
          currentConversationId={conversationId}
          onConversationChange={setConversationId}
        />

      </Sider>

      <Layout>

        <ChatHeader />

        <Content
          style={{
            display: "flex",
            flexDirection: "column",
            padding: 20,
            background: "#f5f5f5",
          }}
        >

          <MessageList
            messages={messages}
          />

          <ChatInput
            loading={loading}
            onSend={handleSend}
          />

        </Content>

      </Layout>

    </Layout>

  );

}