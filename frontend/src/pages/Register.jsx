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

const { Title, Text } = Typography;

function Register() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const onFinish = async (values) => {
    try {
      setLoading(true);

      const data = {
        username: values.username,
        nickname: values.nickname,
        password: values.password,
      };

      await register(data);

      message.success("注册成功，请登录");

      navigate("/login");
    } catch (error) {
      message.error(
        error.response?.data?.detail || "注册失败"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "#f5f5f5",
      }}
    >
      <Card
        style={{
          width: 420,
          borderRadius: 12,
          boxShadow: "0 8px 24px rgba(0,0,0,.08)",
        }}
      >
        <Title
          level={2}
          style={{
            textAlign: "center",
            marginBottom: 8,
          }}
        >
          Travel AI
        </Title>

        <Text
          type="secondary"
          style={{
            display: "block",
            textAlign: "center",
            marginBottom: 30,
          }}
        >
          创建你的账号
        </Text>

        <Form
          layout="vertical"
          onFinish={onFinish}
          autoComplete="off"
        >
          <Form.Item
            label="用户名"
            name="username"
            rules={[
              {
                required: true,
                message: "请输入用户名",
              },
            ]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="请输入用户名"
              size="large"
            />
          </Form.Item>

          <Form.Item
            label="昵称"
            name="nickname"
            rules={[
              {
                required: true,
                message: "请输入昵称",
              },
            ]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="请输入昵称"
              size="large"
            />
          </Form.Item>

          <Form.Item
            label="密码"
            name="password"
            rules={[
              {
                required: true,
                message: "请输入密码",
              },
              {
                min: 6,
                message: "密码长度不能少于6位",
              },
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="请输入密码"
              size="large"
            />
          </Form.Item>

          <Form.Item
            label="确认密码"
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
              prefix={<LockOutlined />}
              placeholder="请再次输入密码"
              size="large"
            />
          </Form.Item>

          <Button
            type="primary"
            htmlType="submit"
            size="large"
            block
            loading={loading}
          >
            注册
          </Button>

          <div
            style={{
              marginTop: 20,
              textAlign: "center",
            }}
          >
            已有账号？
            <Link to="/login">
              立即登录
            </Link>
          </div>
        </Form>
      </Card>
    </div>
  );
}

export default Register;