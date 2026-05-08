import axios from "axios";
import { API_BASE_URL } from "./constants";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  registerStudent: (data: {
    full_name: string;
    email: string;
    phone: string;
    password: string;
    confirm_password: string;
    date_of_birth?: string;
    gender?: string;
    address?: string;
    pincode?: string;
  }) => apiClient.post("/auth/register/student", data),

  registerInstitution: (data: {
    institution_name: string;
    email: string;
    phone: string;
    password: string;
    confirm_password: string;
    address: string;
    district: string;
    state: string;
    pincode: string;
  }) => apiClient.post("/auth/register/institution", data),

  login: (email: string, password: string) =>
    apiClient.post("/auth/login", { email, password }),

  refresh: (refreshToken: string) =>
    apiClient.post("/auth/refresh", { refresh_token: refreshToken }),

  logout: () => apiClient.post("/auth/logout"),
};

export const setAuthToken = (token: string) => {
  if (typeof window !== "undefined") {
    localStorage.setItem("token", token);
    apiClient.defaults.headers.Authorization = `Bearer ${token}`;
  }
};

export const removeAuthToken = () => {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token");
    delete apiClient.defaults.headers.Authorization;
  }
};

export const getAuthToken = () => {
  if (typeof window !== "undefined") {
    return localStorage.getItem("token");
  }
  return null;
};

export default apiClient;
