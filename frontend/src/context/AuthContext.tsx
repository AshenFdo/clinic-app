import { createContext, useEffect, useState, type ReactNode } from "react";
import { authApi } from "../api/auth.api";
import { tokenStorage } from "../utils/tokenStorage";
import { type LoginPayload, type User, type RegisterPayload , type GuestUser} from "../types/auth";


interface AuthContextValue {
  user: User | null;
  isLoading: boolean;
  login: (p: LoginPayload) => Promise<void>;
  register: (p: RegisterPayload) => Promise<void>;
  verifyOtp: (email: string, otp: string) => Promise<void>;
  resendOtp: (email: string) => Promise<void>;
  logout: () => Promise<void>;
  createGuestUser: (p: GuestUser) => Promise<void>;
};


export const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // restore session on reload
  useEffect(() => {
    if (!tokenStorage.getAccess()) return setIsLoading(false);
    authApi.me().then(setUser).catch(() => tokenStorage.clear()).finally(() => setIsLoading(false));
  }, []);

  const login = async (p: LoginPayload) => {
    const data = await authApi.login(p);
    tokenStorage.set(data.access_token, data.refresh_token);
    setUser(data.user);
    console.log(data.user);
  };

  const register = async (p: RegisterPayload) => {
    await authApi.register(p);
  };

  const logout = async () => {
    try { await authApi.logout(); } finally {
      tokenStorage.clear();
      setUser(null);
    }
  };
  const verifyOtp = async (email: string, otp: string) => {
    const data = await authApi.verifyOtp(email, otp);
    tokenStorage.set(data.access_token, data.refresh_token);
    setUser(data.user);
  };

  const resendOtp = async (email: string) => {
    await authApi.resendOtp(email);
  };

  const createGuestUser = async (p: GuestUser) => {
    const data = await authApi.createGuest(p);
    tokenStorage.set(data.access_token, data.refresh_token);
    setUser(data.user);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout, verifyOtp, resendOtp, createGuestUser }}>
      {children}
    </AuthContext.Provider>
  );
}