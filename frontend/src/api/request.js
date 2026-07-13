import axios from "axios";

const request = axios.create({
  baseURL: "http://127.0.0.1:8001/api",
  timeout: 30000,
});

request.interceptors.request.use((config) => {

  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

request.interceptors.response.use(

  (response) => response,

  (error) => {

    if (error.response?.status === 401) {

      localStorage.removeItem("token");

      localStorage.removeItem("user");

      // 不在这里强制跳转，让组件自己处理错误显示

    }

    return Promise.reject(error);

  }

);

export default request;