import { createContext,useContext, useState, useEffect } from "react";


// ─── Context ──────────────────────────────────────────────────────────────
const AuthContext = createContext(null);
 
// ─── Provider ─────────────────────────────────────────────────────────────
// Wrap your entire app with this in main.jsx.
// Stores the logged-in user and JWT token globally.
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);       // { user_id, role, email, full_name, ... }
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true); // true while reading from localStorage on mount
 
  // On first load, restore session from localStorage
  useEffect(() => {
    const storedToken = localStorage.getItem("access_token");
    const storedUser = localStorage.getItem("user");
 
    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);
 
  // Called after successful login or OTP verification
  const login = (tokenData, userData) => {
    localStorage.setItem("access_token", tokenData);
    localStorage.setItem("user", JSON.stringify(userData));
    setToken(tokenData);
    setUser(userData);
  };
 
  // Called on logout
  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    setToken(null);
    setUser(null);
  };
 
  const value = {
    user,
    token,
    loading,
    isAuthenticated: !!token,
    role: user?.role || null, // "admin" | "doctor" | "patient"
    login,
    logout,
  };
 
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
 
// ─── Hook ─────────────────────────────────────────────────────────────────
// Use this anywhere: const { user, login, logout } = useAuthContext();
export const useAuthContext = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuthContext must be used inside <AuthProvider>");
  }
  return context;
};
 