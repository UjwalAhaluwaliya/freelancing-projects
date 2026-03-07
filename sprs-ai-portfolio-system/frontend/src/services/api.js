import axios from "axios";
import { clearSession, getToken } from "../utils/auth";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:5000",
  headers: {
    "Content-Type": "application/json"
  },
  timeout: 20000
});

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const fallbackMessage = "Unable to connect to server. Check backend service and API URL.";

    if (error.response?.status === 401) {
      clearSession();
    }

    if (!error.response) {
      return Promise.reject(new Error(fallbackMessage));
    }
    return Promise.reject(error);
  }
);

export default api;
