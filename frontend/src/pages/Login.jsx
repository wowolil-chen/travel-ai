import { useEffect, useState } from "react";
import { Button, Card, Form, Input, Typography } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import { Link, useNavigate } from "react-router-dom";

import { login } from "../api/auth";
import { saveLogin } from "../utils/storage";
import weBg from "../assets/we.jpg";
import meBg from "../assets/me.jpg";

const MOBILE_BREAKPOINT = 768;

const { Title, Text } = Typography;

// 错误信息翻译
function translateError(msg, fieldName) {
  if (!msg) return msg;
  
  // 根据字段名和错误信息生成更具体的提示
  if (msg.includes("at least 3 characters")) {
    if (fieldName === "username") return "用户名长度不能少于 3 个字符";
    if (fieldName === "password") return "密码长度不能少于 3 个字符";
  }
  if (msg.includes("at least 6 characters")) {
    if (fieldName === "username") return "用户名长度不能少于 6 个字符";
    if (fieldName === "password") return "密码长度不能少于 6 个字符";
  }
  
  const translations = {
    "Username or password is incorrect": "用户名或密码错误",
    "User not found": "用户不存在",
    "Invalid credentials": "凭证无效",
  };
  return translations[msg] || msg;
}

function Login() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [isMobile, setIsMobile] = useState(
    window.innerWidth < MOBILE_BREAKPOINT
  );

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < MOBILE_BREAKPOINT);
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const onFinish = async (values) => {
    try {
      setLoading(true);
      setErrorMsg("");

      const res = await login(values);

      const data = res.data;

      // 保存登录信息
      saveLogin(data);

      // 跳转聊天页面
      navigate("/chat");
    } catch (error) {
      console.error("Login error:", error);
      let msg = "用户名或密码错误";
      const data = error.response?.data;
      if (data?.detail) {
        if (Array.isArray(data.detail)) {
          msg = data.detail.map((d) => {
            const fieldName = d.loc?.[d.loc.length - 1];
            return translateError(d.msg, fieldName);
          }).join("; ");
        } else if (typeof data.detail === "string") {
          msg = translateError(data.detail);
        }
      } else if (data?.message) {
        msg = translateError(data.message);
      } else if (error.message) {
        msg = translateError(error.message);
      }
      setErrorMsg(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <style>{`
        .login-page input::placeholder {
          color: rgba(255, 255, 255, 0.85) !important;
          font-weight: 500;
        }
      `}</style>
      <div
        className="login-page"
        style={{
          height: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          backgroundImage: `url(${isMobile ? meBg : weBg})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
        }}
      >
      <Card
        styles={{ body: { background: "transparent" } }}
        style={{
          width: 420,
          borderRadius: 16,
          background: "transparent",
          boxShadow: "none",
          border: "2px solid rgba(255, 255, 255, 0.6)",
        }}
      >
        <Title
          level={2}
          style={{
            textAlign: "center",
            marginBottom: 8,
            color: "#fff",
            textShadow: "0 2px 6px rgba(0,0,0,0.5)",
            fontWeight: 700,
          }}
        >
          Travel AI
        </Title>

        <Text
          style={{
            display: "block",
            textAlign: "center",
            marginBottom: 30,
            color: "#fff",
            textShadow: "0 2px 6px rgba(0,0,0,0.5)",
            fontWeight: 500,
          }}
        >
          智能旅游规划助手
        </Text>

        {errorMsg && (
          <div
            style={{
              background: "rgba(255, 77, 79, 0.15)",
              border: "1px solid rgba(255, 77, 79, 0.5)",
              borderRadius: 8,
              padding: "10px 16px",
              marginBottom: 20,
              color: "#fff",
              textShadow: "0 1px 3px rgba(0,0,0,0.5)",
              fontWeight: 500,
              textAlign: "center",
            }}
          >
            {errorMsg}
          </div>
        )}

        <Form
          layout="vertical"
          onFinish={onFinish}
          autoComplete="off"
        >
          <Form.Item
            label={<span style={{ color: "#fff", textShadow: "0 1px 4px rgba(0,0,0,0.5)", fontWeight: 500 }}>用户名</span>}
            name="username"
            rules={[
              {
                required: true,
                message: "请输入用户名",
              },
            ]}
          >
            <Input
              prefix={<UserOutlined style={{ color: "#fff", textShadow: "0 1px 3px rgba(0,0,0,0.4)" }} />}
              placeholder="请输入用户名"
              size="large"
              style={{
                background: "transparent",
                border: "1px solid rgba(255,255,255,0.5)",
                color: "#fff",
                textShadow: "0 1px 3px rgba(0,0,0,0.4)",
                fontWeight: 500,
              }}
            />
          </Form.Item>

          <Form.Item
            label={<span style={{ color: "#fff", textShadow: "0 1px 4px rgba(0,0,0,0.5)", fontWeight: 500 }}>密码</span>}
            name="password"
            rules={[
              {
                required: true,
                message: "请输入密码",
              },
            ]}
          >
            <Input.Password
              prefix={<LockOutlined style={{ color: "#fff", textShadow: "0 1px 3px rgba(0,0,0,0.4)" }} />}
              placeholder="请输入密码"
              size="large"
              style={{
                background: "transparent",
                border: "1px solid rgba(255,255,255,0.5)",
                color: "#fff",
                textShadow: "0 1px 3px rgba(0,0,0,0.4)",
                fontWeight: 500,
              }}
            />
          </Form.Item>

          <Button
            type="primary"
            htmlType="submit"
            size="large"
            block
            loading={loading}
            style={{
              background: "transparent",
              border: "1px solid rgba(255,255,255,0.6)",
              color: "#fff",
              fontWeight: 600,
            }}
          >
            登录
          </Button>

          <div
            style={{
              textAlign: "center",
              marginTop: 20,
              color: "#fff",
              textShadow: "0 1px 4px rgba(0,0,0,0.5)",
              fontWeight: 500,
            }}
          >
            没有账号？
            <Link to="/register" style={{ color: "#fff", fontWeight: 700, textShadow: "0 1px 4px rgba(0,0,0,0.5)" }}>立即注册</Link>
          </div>
        </Form>
      </Card>
    </div>
    </>
  );
}

export default Login;