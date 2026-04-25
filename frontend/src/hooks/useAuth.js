import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthContext } from "../context/AuthContext";
import {
  registerUser,
  verifyOtp,
  resendOtp,
  loginUser,
  forgotPassword,
  resetPassword,
  getCurrentUser,
} from "../api/auth.api";

// ─── useAuth ──────────────────────────────────────────────────────────────
// Central hook for all auth operations.
// Each operation returns { success, error } so the UI can respond.
export const useAuth = () => {
  const { login, logout } = useAuthContext();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Clears error before each operation
  const clearError = () => setError(null);

  // ── Register ─────────────────────────────────────────────────────────────
  // On success, backend sends OTP to email.
  // We return the email so Register.jsx can advance to the OTP step.
  const register = async (formData) => {
    clearError();
    setLoading(true);
    try {
      await registerUser({
        full_name: formData.fullName,
        email: formData.email,
        password: formData.password,
        gender: formData.gender,
        mobile_no: formData.mobileNo,
        date_of_birth: formData.dateOfBirth, // "YYYY-MM-DD"
        role: "patient", // registration is always for patients
      });
      return { success: true };
    } catch (err) {
      const msg = err.response?.data?.detail || "Registration failed.";
      setError(msg);
      return { success: false, error: msg };
    } finally {
      setLoading(false);
    }
  };

  // ── Verify OTP (after register) ──────────────────────────────────────────
  // On success, backend returns tokens + user → we call login() to store them.
  const verifyRegistrationOtp = async (email, otp) => {
    clearError();
    setLoading(true);
    try {
      const data = await verifyOtp({ email, otp });
      // data = { access_token, token_type, user: { user_id, role, ... } }
      if (!data?.access_token || !data?.user) {
        throw new Error("Verification succeeded but no session data was returned.");
      }
      login(data.access_token, data.user);
      navigate("/user_sample");
      return { success: true };
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || "Invalid or expired OTP.";
      setError(msg);
      return { success: false, error: msg };
    } finally {
      setLoading(false);
    }
  };

  // ── Resend OTP ───────────────────────────────────────────────────────────
  const resendRegistrationOtp = async (email) => {
    clearError();
    setLoading(true);
    try {
      await resendOtp({ email });
      return { success: true };
    } catch (err) {
      const msg = err.response?.data?.detail || "Could not resend OTP.";
      setError(msg);
      return { success: false, error: msg };
    } finally {
      setLoading(false);
    }
  };

  // ── Login ─────────────────────────────────────────────────────────────────
  const loginWithCredentials = async (email, password) => {
    clearError();
    setLoading(true);
    try {
      const data = await loginUser({ email, password });
      login(data.access_token, data.user);

      // Redirect based on role
      const roleRoutes = {
        admin: "/admin/dashboard",
        doctor: "/doctor/dashboard",
        patient: "/patient/dashboard",
      };
      navigate(roleRoutes[data.user.role] || "/");
      return { success: true };
    } catch (err) {
      const msg = err.response?.data?.detail || "Login failed.";
      setError(msg);
      return { success: false, error: msg };
    } finally {
      setLoading(false);
    }
  };

  // ── Forgot Password ───────────────────────────────────────────────────────
  const sendForgotPasswordOtp = async (email) => {
    clearError();
    setLoading(true);
    try {
      await forgotPassword({ email });
      return { success: true };
    } catch (err) {
      const msg = err.response?.data?.detail || "Email not found.";
      setError(msg);
      return { success: false, error: msg };
    } finally {
      setLoading(false);
    }
  };

  // ── Reset Password ────────────────────────────────────────────────────────
  const resetUserPassword = async (email, otp, newPassword) => {
    clearError();
    setLoading(true);
    try {
      await resetPassword({ email, otp, new_password: newPassword });
      navigate("/login");
      return { success: true };
    } catch (err) {
      const msg = err.response?.data?.detail || "Could not reset password.";
      setError(msg);
      return { success: false, error: msg };
    } finally {
      setLoading(false);
    }
  };

  // ── Logout ────────────────────────────────────────────────────────────────
  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  // __get_user_data____
  const getUserData = () => {
      return getCurrentUser();
  };

  return {
    loading,
    error,
    clearError,
    register,
    verifyRegistrationOtp,
    resendRegistrationOtp,
    loginWithCredentials,
    sendForgotPasswordOtp,
    resetUserPassword,
    getUserData,
    logout: handleLogout,
  };
};