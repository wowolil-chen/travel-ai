import { useState } from "react";
import {
  Button,
  Card,
  Form,
  Input,
  Typography,
  message,
} from "antd";
import {
  UserOutlined,
  LockOutlined,
} from "@ant-design/icons";
import {
  Link,
  useNavigate,
} from "react-router-dom";

import { register } from "../api/auth";
import weBg from "../assets/we.jpg";

const { Title, Text } = Typography;

// 错误信息翻译
function translateError(msg, fieldName) {
  if (!msg) return msg;
  
  // 根据字段名和错误信息生成更具体的提示
  if (msg.includes("at least 3 characters")) {
    if (fieldName === "username") return "用户名长度不能少于 3 个字符";
    if (fieldName === "password") return "密码长度不能少于 3 个字符";
    if (fieldName === "nickname") return "昵称长度不能少于 3 个字符";
  }
  if (msg.includes("at least 6 characters")) {
    if (fieldName === "username") return "用户名长度不能少于 6 个字符";
    if (fieldName === "password") return "密码长度不能少于 6 个字符";
    if (fieldName === "nickname") return "昵称长度不能少于 6 个字符";
  }
  
  const translations = {
    "Username or password is incorrect": "用户名或密码错误",
    "User not found": "用户不存在",
    "Invalid credentials": "凭证无效",
    "Username already exists": "用户名已存在",
  };
  return translations[msg] || msg;
}

function Register() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const onFinish = async (values) => {
    try {
      setLoading(true);
      setErrorMsg("");

      const data = {
        username: values.username,
        nickname: values.nickname,
        password: values.password,
      };

      await register(data);

      message.success("注册成功，请登录");

      navigate("/login");
    } catch (error) {
      let msg = "注册失败";
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
        .register-page input::placeholder {
          color: rgba(255, 255, 255, 0.85) !important;
          font-weight: 500;
        }
      `}</style>
      <div
        className="register-page"
        style={{
          height: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          backgroundImage: `url(${weBg})`,
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
          创建你的账号
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
              {
                min: 3,
                message: "用户名长度不能少于3个字符",
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
            label={<span style={{ color: "#fff", textShadow: "0 1px 4px rgba(0,0,0,0.5)", fontWeight: 500 }}>昵称</span>}
            name="nickname"
            rules={[
              {
                required: true,
                message: "请输入昵称",
              },
              {
                min: 3,
                message: "昵称长度不能少于3个字符",
              },
            ]}
          >
            <Input
              prefix={<UserOutlined style={{ color: "#fff", textShadow: "0 1px 3px rgba(0,0,0,0.4)" }} />}
              placeholder="请输入昵称"
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
              {
                min: 6,
                message: "密码长度不能少于6个字符",
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

          <Form.Item
            label={<span style={{ color: "#fff", textShadow: "0 1px 4px rgba(0,0,0,0.5)", fontWeight: 500 }}>确认密码</span>}
            name="confirmPassword"
            dependencies={["password"]}
            rules={[
              {
                required: true,
                message: "请再次输入密码",
              },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (
                    !value ||
                    getFieldValue("password") === value
                  ) {
                    return Promise.resolve();
                  }

                  return Promise.reject(
                    new Error("两次密码输入不一致")
                  );
                },
              }),
            ]}
          >
            <Input.Password
              prefix={<LockOutlined style={{ color: "#fff", textShadow: "0 1px 3px rgba(0,0,0,0.4)" }} />}
              placeholder="请再次输入密码"
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
            注册
          </Button>

          <div
            style={{
              marginTop: 20,
              textAlign: "center",
              color: "#fff",
              textShadow: "0 1px 4px rgba(0,0,0,0.5)",
              fontWeight: 500,
            }}
          >
            已有账号？
            <Link to="/login" style={{ color: "#fff", fontWeight: 700, textShadow: "0 1px 4px rgba(0,0,0,0.5)" }}>
              立即登录
            </Link>
          </div>
        </Form>
      </Card>
    </div>
    </>
  );
}

export default Register;