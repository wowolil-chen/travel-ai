import { useEffect, useState } from "react";
import {
  Button,
  Typography,
  List,
  Popconfirm,
  message,
} from "antd";
import {
  PlusOutlined,
  DeleteOutlined,
} from "@ant-design/icons";

import {
  createConversation,
  getConversationList,
  deleteConversation,
} from "../api/chat";

const { Title } = Typography;

function Sidebar({
  currentConversationId,
  onConversationChange,
  onConversationSelect,
}) {
  const [conversations, setConversations] = useState([]);

  /**
   * 加载会话列表
   */
  const loadConversationList = async () => {
    try {
      const res = await getConversationList();
      setConversations(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  /**
   * 新建聊天
   */
  const handleCreateConversation = async () => {
    try {
      const res = await createConversation();

      message.success("创建成功");

      await loadConversationList();

      if (onConversationChange) {
        onConversationChange(res.data.id);
      }
    } catch (e) {
      message.error("创建失败");
    }
  };

  /**
   * 删除聊天
   */
  const handleDeleteConversation = async (id) => {
    try {
      await deleteConversation(id);

      message.success("删除成功");

      await loadConversationList();

      if (currentConversationId === id) {
        onConversationChange(null);
      }
    } catch (e) {
      message.error("删除失败");
    }
  };

  useEffect(() => {
    loadConversationList();
  }, []);

  return (
    <div
      style={{
        height: "100%",
        padding: 20,
        display: "flex",
        flexDirection: "column",
      }}
    >
      <Title level={4}>
        Travel AI
      </Title>

      <Button
        type="primary"
        icon={<PlusOutlined />}
        block
        onClick={handleCreateConversation}
      >
        新建聊天
      </Button>

      <List
        style={{
          marginTop: 20,
          overflow: "auto",
          flex: 1,
        }}
        dataSource={conversations}
        renderItem={(item) => (
          <List.Item
            style={{
              cursor: "pointer",
              background:
                currentConversationId === item.id
                  ? "#e6f4ff"
                  : "",
              borderRadius: 6,
              padding: "8px 12px",
            }}
            onClick={() => {
              onConversationChange(item.id);
              if (onConversationSelect) {
                onConversationSelect();
              }
            }}
            actions={[
              <Popconfirm
                title="确定删除吗？"
                onConfirm={() =>
                  handleDeleteConversation(item.id)
                }
              >
                <DeleteOutlined />
              </Popconfirm>,
            ]}
          >
            {item.title}
          </List.Item>
        )}
      />
    </div>
  );
}

export default Sidebar;