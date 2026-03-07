import { createContext, useContext, useMemo, useState } from "react";
import api from "../lib/api";
import { clearToken, getRoleFromToken, getToken, saveToken } from "../lib/auth";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const existingToken = getToken();
  const [token, setToken] = useState(existingToken);
  const [role, setRole] = useState(existingToken ? getRoleFromToken(existingToken) : null);
  const [loading, setLoading] = useState(false);
  const isAuthenticated = Boolean(token);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const response = await api.post("/auth/login", null, {
        params: { email, password },
      });
      const accessToken = response.data?.access_token;
      if (!accessToken) {
        throw new Error("Token not received");
      }
      saveToken(accessToken);
      setToken(accessToken);
      setRole(getRoleFromToken(accessToken));
      return { success: true };
    } catch (error) {
      return {
        success: false,
        message: error?.response?.data?.detail || "Login failed",
      };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    clearToken();
    setToken(null);
    setRole(null);
  };

  const value = useMemo(
    () => ({
      token,
      role,
      loading,
      isAuthenticated,
      login,
      logout,
    }),
    [token, role, loading, isAuthenticated],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}
