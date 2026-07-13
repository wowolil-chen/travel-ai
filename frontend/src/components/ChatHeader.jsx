import { Avatar, Button, Space, Typography } from "antd";
import {
  MenuOutlined,
  UserOutlined,
  LogoutOutlined,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";

import { logout, getUser } from "../utils/storage";

const { Title } = Typography;

function ChatHeader({ onMenuClick, isMobile }) {
  const navigate = useNavigate();

  const user = getUser();

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
        padding: "0 16px",
        borderBottom: "1px solid #f0f0f0",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        background: "#fff",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <Button
          icon={<MenuOutlined />}
          onClick={onMenuClick}
          style={{
            display: isMobile ? "flex" : "none",
          }}
        />
        <Title
          level={4}
          style={{
            margin: 0,
            fontSize: isMobile ? 16 : 18,
          }}
        >
          Travel AI
        </Title>
      </div>

      <Space size={isMobile ? 8 : 16}>
        <Avatar
          size={isMobile ? 32 : 40}
          icon={<UserOutlined />}
        />

        {!isMobile && (
          <span>{user?.nickname || user?.username || "用户"}</span>
        )}

        <Button
          danger
          icon={<LogoutOutlined />}
          onClick={handleLogout}
          size={isMobile ? "small" : "middle"}
        >
          {isMobile ? "" : "退出登录"}
        </Button>
      </Space>
    </div>
  );
}

export default ChatHeader;