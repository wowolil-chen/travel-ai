import { Button, Typography } from "antd";
import { PlusOutlined } from "@ant-design/icons";

const { Title } = Typography;

function Sidebar() {
  return (
    <div
      style={{
        padding: 20,
      }}
    >
      <Title level={4}>Travel AI</Title>

      <Button
        type="primary"
        icon={<PlusOutlined />}
        block
      >
        新建聊天
      </Button>
    </div>
  );
}

export default Sidebar;