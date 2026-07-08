import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Chat from "./pages/Chat";
import History from "./pages/History";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 默认跳到登录 */}
        <Route path="/" element={<Navigate to="/login" />} />

        <Route path="/login" element={<Login />} />

        <Route path="/register" element={<Register />} />

        <Route path="/chat" element={<Chat />} />

        <Route path="/history" element={<History />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;