"use client";
import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import axios from "axios";

interface User {
  token: string;
  email?: string;
  nome?: string;
}

interface AuthContextType {
  user: User | null;
  login: (credentials: { email: string; senha: string }) => Promise<void>;
  loginWithGoogle: () => void;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Verifica token normal
    const token = localStorage.getItem("token");
    if (token) {
      setUser({ token });
    }

    // Captura token vindo do callback do Google (via query param ?token=...)
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      const googleToken = params.get("token");
      if (googleToken) {
        localStorage.setItem("token", googleToken);
        setUser({ token: googleToken });
        // Limpa o token da URL para não ficar exposto
        window.history.replaceState({}, "", window.location.pathname);
      }
    }

    setLoading(false);
  }, []);

  const login = async (credentials: { email: string; senha: string }) => {
    const formData = new URLSearchParams();
    formData.append("username", credentials.email);
    formData.append("password", credentials.senha);

    const response = await axios.post(
      "http://localhost:8000/api/auth/login",
      formData,
      { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
    );

    const token = response.data.access_token;
    localStorage.setItem("token", token);
    setUser({ token });
  };

  const loginWithGoogle = () => {
    window.location.href = "http://localhost:8000/api/auth/google/login";
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, loginWithGoogle, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);