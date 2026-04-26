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
// Backend expects JSON body { email, password } and returns { access_token, token_type }.
export const loginUser = async ({ email, password }) => {
  const response = await apiClient.post("/auth/login", { email, password });
  return response.data; // { access_token, token_type }
};
 
// ─── Forgot Password ──────────────────────────────────────────────────────
// POST /auth/forgot-password
// Backend sends a password reset OTP to the email.
export const forgotPassword = async ({ email }) => {
  const response = await apiClient.post("/auth/forgot-password", { email });
  return response.data;
};

// ─── Verify Reset OTP ─────────────────────────────────────────────────────
// POST /auth/verify-reset-otp
// Validates password reset OTP and returns recovery session tokens.
export const verifyResetOtp = async ({ email, otp }) => {
  const response = await apiClient.post("/auth/verify-reset-otp", { email, otp });
  return response.data;
};
 
// ─── Reset Password ───────────────────────────────────────────────────────
// POST /auth/reset-password
// Uses verified recovery tokens to set a new password.
export const resetPassword = async ({ access_token, refresh_token, new_password, confirm_password }) => {
  const response = await apiClient.post("/auth/reset-password", {
    access_token,
    refresh_token,
    new_password,
    confirm_password,
  });
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await apiClient.get("/users/me");
  return response.data;
}