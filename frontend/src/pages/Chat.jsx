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

const MOBILE_BREAKPOINT = 768;

export default function Chat() {

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const [conversationId, setConversationId] = useState(null);

  const [sidebarCollapsed, setSidebarCollapsed] = useState(
    window.innerWidth < MOBILE_BREAKPOINT
  );

  const [isMobile, setIsMobile] = useState(
    window.innerWidth < MOBILE_BREAKPOINT
  );

  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < MOBILE_BREAKPOINT;
      setIsMobile(mobile);
      if (!mobile) {
        setSidebarCollapsed(false);
      }
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

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
        style={{
          position: isMobile ? "fixed" : "relative",
          zIndex: 1000,
          height: "100vh",
          transform: isMobile && sidebarCollapsed ? "translateX(-100%)" : "translateX(0)",
          transition: "transform 0.3s ease",
          boxShadow: "2px 0 8px rgba(0,0,0,.1)",
        }}
      >

        <Sidebar
          currentConversationId={conversationId}
          onConversationChange={setConversationId}
          onConversationSelect={() => {
            if (isMobile) {
              setSidebarCollapsed(true);
            }
          }}
        />

      </Sider>

      {isMobile && !sidebarCollapsed && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: "rgba(0,0,0,.5)",
            zIndex: 999,
            onClick: () => setSidebarCollapsed(true),
          }}
        />
      )}

      <Layout
        style={{
          marginLeft: isMobile ? 0 : 280,
        }}
      >

        <ChatHeader onMenuClick={toggleSidebar} isMobile={isMobile} />

        <Content
          style={{
            display: "flex",
            flexDirection: "column",
            padding: isMobile ? 10 : 20,
            background: "#f5f5f5",
            minHeight: "calc(100vh - 64px)",
          }}
        >

          <MessageList
            messages={messages}
            isMobile={isMobile}
          />

          <ChatInput
            loading={loading}
            onSend={handleSend}
            isMobile={isMobile}
          />

        </Content>

      </Layout>

    </Layout>

  );

}