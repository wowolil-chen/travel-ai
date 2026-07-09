import { Layout } from "antd";

const { Sider, Content } = Layout;

function ChatLayout({ sidebar, content }) {
  return (
    <Layout style={{ height: "100vh" }}>
      <Sider
        width={280}
        theme="light"
        style={{
          borderRight: "1px solid #f0f0f0",
        }}
      >
        {sidebar}
      </Sider>

      <Content
        style={{
          background: "#fff",
        }}
      >
        {content}
      </Content>
    </Layout>
  );
}

export default ChatLayout;