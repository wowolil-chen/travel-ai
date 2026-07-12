import { Layout } from "antd";

const { Sider, Content } = Layout;

function ChatLayout({
  sidebar,
  header,
  content,
}) {
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
          borderRight: "1px solid #f0f0f0",
        }}
      >
        {sidebar}
      </Sider>

      <Layout>
        {header}

        <Content
          style={{
            display: "flex",
            flexDirection: "column",
            padding: 20,
            background: "#f5f5f5",
          }}
        >
          {content}
        </Content>
      </Layout>
    </Layout>
  );
}

export default ChatLayout;