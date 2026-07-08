import axios from "axios";
import { getToken } from "../utils/storage";

const request = axios.create({
  baseURL: "http://127.0.0.1:8001/api",
  timeout: 10000,
});

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const token = getToken();

    // 如果存在 Token，则自动携带
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // 以后可以统一处理 401、403、500 等错误
    // 例如：
    // if (error.response?.status === 401) {
    //   clearLogin();
    //   window.location.href = "/login";
    // }

    return Promise.reject(error);
  }
);

export default request;