import { useEffect, useRef, useState } from "react";
import {
  Button,
  Input,
  Layout,
  List,
  message,
  Typography,
} from "antd";
import { SendOutlined } from "@ant-design/icons";

import Sidebar from "../components/Sidebar";

import {
  streamChat,
  getMessages,
} from "../api/chat";

const { Sider, Content } = Layout;
const { Text } = Typography;
const { TextArea } = Input;

export default function Chat() {

  const [messages, setMessages] = useState([]);

  const [input, setInput] = useState("");

  const [loading, setLoading] = useState(false);

  const [conversationId, setConversationId] = useState(null);

  const messageEndRef = useRef(null);

  // 自动滚动
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  // 切换聊天
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
  const handleSend = async () => {

    if (!conversationId) {

      message.warning("请先创建聊天");

      return;

    }

    if (!input.trim() || loading) return;

    const question = input.trim();

    setInput("");

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

  /**
   * Enter发送
   */
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

        <Content

          style={{

            display: "flex",

            flexDirection: "column",

            padding: 20,

            background: "#f5f5f5",

          }}

        >

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

            <div ref={messageEndRef} />

          </div>

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

        </Content>

      </Layout>

    </Layout>

  );

}