import { Avatar, Button, Space, Typography } from "antd";
import {
  UserOutlined,
  LogoutOutlined,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";

import { logout } from "../utils/storage";

const { Title } = Typography;

function ChatHeader() {
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();

    navigate("/login", {
      replace: true,
    });
  };

  return (
    <div
      style={{
        height: 64,
        padding: "0 24px",
        borderBottom: "1px solid #f0f0f0",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        background: "#fff",
      }}
    >
      <Title
        level={4}
        style={{
          margin: 0,
        }}
      >
        Travel AI
      </Title>

      <Space size={16}>
        <Avatar
          size={40}
          icon={<UserOutlined />}
        />

        <span>管理员</span>

        <Button
          danger
          icon={<LogoutOutlined />}
          onClick={handleLogout}
        >
          退出登录
        </Button>
      </Space>
    </div>
  );
}

export default ChatHeader;