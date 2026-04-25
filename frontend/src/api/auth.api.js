import apiClient from "./client.js";

// ─── Register ──────────────────────────────────────────────────────────────
// POST /auth/register
// Sends user details. Backend creates user with is_active=False
// and sends an OTP to the email.
export const registerUser = async (userData) => {
    const response = await apiClient.post('/auth/register-patient', userData);
    return response.data;
}

// ─── Verify OTP ───────────────────────────────────────────────────────────
// POST /auth/verify-otp
// Confirms the OTP code. Backend sets is_active=True and returns JWT tokens.
export const verifyOtp = async ({ email, otp }) => {
  const response = await apiClient.post("/auth/verify-otp", { email, otp });
  return response.data;
};
 
// ─── Resend OTP ───────────────────────────────────────────────────────────
// POST /auth/resend-otp
// Sends a fresh OTP to the email if the previous one expired.
export const resendOtp = async ({ email }) => {
  const response = await apiClient.post("/auth/resend-otp", { email });
  return response.data;
};
 
// ─── Login ────────────────────────────────────────────────────────────────
// POST /auth/login
// FastAPI expects form data (OAuth2PasswordRequestForm) by default.
// We send as URLSearchParams to match that.
export const loginUser = async ({ email, password }) => {
  const formData = new URLSearchParams();
  formData.append("username", email); // FastAPI OAuth2 uses "username"
  formData.append("password", password);
 
  const response = await apiClient.post("/auth/login", formData, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return response.data; // { access_token, token_type, user }
};
 
// ─── Forgot Password ──────────────────────────────────────────────────────
// POST /auth/forgot-password
// Backend sends a password reset OTP to the email.
export const forgotPassword = async ({ email }) => {
  const response = await apiClient.post("/auth/forgot-password", { email });
  return response.data;
};
 
// ─── Reset Password ───────────────────────────────────────────────────────
// POST /auth/reset-password
// Verifies the reset OTP and sets a new password.
export const resetPassword = async ({ email, otp, new_password }) => {
  const response = await apiClient.post("/auth/reset-password", {
    email,
    otp,
    new_password,
  });
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await apiClient.get("/users/me");
  return response.data;
}