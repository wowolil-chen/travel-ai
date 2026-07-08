// 保存登录信息
export function saveLogin(data) {
  localStorage.setItem("token", data.access_token);
  localStorage.setItem("user", JSON.stringify(data.user));
}

export function getToken() {
  return localStorage.getItem("token");
}

export function getUser() {
  const user = localStorage.getItem("user");
  return user ? JSON.parse(user) : null;
}

export function clearLogin() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
}