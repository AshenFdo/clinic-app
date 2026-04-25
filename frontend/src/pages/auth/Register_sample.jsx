import { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  Box,
  TextField,
  Button,
  Typography,
  MenuItem,
  InputAdornment,
  IconButton,
  Alert,
  CircularProgress,
  LinearProgress,
} from "@mui/material";
import {
  Visibility,
  VisibilityOff,
  PersonOutlined,
  EmailOutlined,
  PhoneOutlined,
  LockOutlined,
} from "@mui/icons-material";
import { useAuth } from "../../hooks/useAuth";

// ─── Constants ────────────────────────────────────────────────────────────
const GENDERS = ["Male", "Female", "Other"];
const OTP_LENGTH = 6;
const OTP_RESEND_SECONDS = 60;

// ─── Step indicator ───────────────────────────────────────────────────────
const steps = ["Your Details", "Verify Email", "All Done"];

// ─── Register Page ────────────────────────────────────────────────────────
export default function Register_sample() {
  const { register, verifyRegistrationOtp, resendRegistrationOtp, loading, error, clearError } = useAuth();

  // Which step we're on: 0 = form, 1 = OTP, 2 = success
  const [step, setStep] = useState(0);
  const [email, setEmail] = useState(""); // carried from step 0 → step 1

  // ── Step 0: Registration form state ──────────────────────────────────────
  const [form, setForm] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
    gender: "",
    mobileNo: "",
    dateOfBirth: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [formErrors, setFormErrors] = useState({});

  // ── Step 1: OTP state ────────────────────────────────────────────────────
  const [otp, setOtp] = useState(Array(OTP_LENGTH).fill(""));
  const [countdown, setCountdown] = useState(OTP_RESEND_SECONDS);
  const [canResend, setCanResend] = useState(false);
  const otpRefs = useRef([]);

  // Countdown timer for OTP resend
  useEffect(() => {
    if (step !== 1) return;
    setCountdown(OTP_RESEND_SECONDS);
    setCanResend(false);
    const interval = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          setCanResend(true);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [step]);

  // ── Handlers ─────────────────────────────────────────────────────────────
  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    if (formErrors[name]) setFormErrors((prev) => ({ ...prev, [name]: "" }));
    clearError();
  };

  const validateForm = () => {
    const errs = {};
    if (!form.fullName.trim()) errs.fullName = "Full name is required";
    if (!form.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) errs.email = "Valid email required";
    if (form.password.length < 8) errs.password = "At least 8 characters";
    if (form.password !== form.confirmPassword) errs.confirmPassword = "Passwords don't match";
    if (!form.gender) errs.gender = "Select a gender";
    if (!form.mobileNo.match(/^\+?[0-9]{9,15}$/)) errs.mobileNo = "Valid phone number required";
    if (!form.dateOfBirth) errs.dateOfBirth = "Date of birth required";
    return errs;
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    const errs = validateForm();
    if (Object.keys(errs).length) { setFormErrors(errs); return; }

    const result = await register(form);
    if (result.success) {
      setEmail(form.email);
      setStep(1);
    }
  };

  // OTP input: handle typing, backspace, paste
  const handleOtpChange = (index, value) => {
    if (!/^\d*$/.test(value)) return; // digits only
    const newOtp = [...otp];
    newOtp[index] = value.slice(-1); // only last char
    setOtp(newOtp);
    clearError();
    if (value && index < OTP_LENGTH - 1) otpRefs.current[index + 1]?.focus();
  };

  const handleOtpKeyDown = (index, e) => {
    if (e.key === "Backspace" && !otp[index] && index > 0) {
      otpRefs.current[index - 1]?.focus();
    }
  };

  const handleOtpPaste = (e) => {
    e.preventDefault();
    const pasted = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, OTP_LENGTH);
    const newOtp = [...otp];
    pasted.split("").forEach((char, i) => { newOtp[i] = char; });
    setOtp(newOtp);
    otpRefs.current[Math.min(pasted.length, OTP_LENGTH - 1)]?.focus();
  };

  const handleOtpSubmit = async (e) => {
    e.preventDefault();
    const code = otp.join("");
    if (code.length < OTP_LENGTH) return;
    const result = await verifyRegistrationOtp(email, code);
    if (result.success) setStep(2);
  };

  const handleResend = async () => {
    if (!canResend) return;
    const result = await resendRegistrationOtp(email);
    if (result.success) {
      setOtp(Array(OTP_LENGTH).fill(""));
      setStep(1); // resets the timer via useEffect
    }
  };

  // ── Progress bar value ────────────────────────────────────────────────────
  const progress = ((step + 1) / steps.length) * 100;

  // ── Render ────────────────────────────────────────────────────────────────
  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        background: "linear-gradient(135deg, #f7fafc 0%, #e8f4f0 50%, #ddeeff 100%)",
        fontFamily: "'Manrope', sans-serif",
      }}
    >
      {/* ── Left panel (decorative, hidden on mobile) ── */}
      <Box
        sx={{
          display: { xs: "none", md: "flex" },
          width: "42%",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "flex-start",
          px: 8,
          py: 6,
          background: "linear-gradient(160deg, #005394 0%, #003a6b 60%, #002244 100%)",
          position: "relative",
          overflow: "hidden",
        }}
      >
        {/* Decorative circles */}
        {[
          { size: 320, top: -80, right: -80, opacity: 0.06 },
          { size: 200, bottom: 60, left: -60, opacity: 0.08 },
          { size: 120, top: "40%", right: 40, opacity: 0.05 },
        ].map((c, i) => (
          <Box
            key={i}
            sx={{
              position: "absolute",
              width: c.size,
              height: c.size,
              borderRadius: "50%",
              border: "2px solid white",
              opacity: c.opacity,
              top: c.top,
              bottom: c.bottom,
              left: c.left,
              right: c.right,
            }}
          />
        ))}

        <Box sx={{ position: "relative", zIndex: 1 }}>
          {/* Logo / Brand */}
          <Box sx={{ display: "flex", alignItems: "center", gap: 1.5, mb: 8 }}>
            <Box
              sx={{
                width: 40, height: 40,
                borderRadius: "10px",
                background: "rgba(255,255,255,0.15)",
                display: "flex", alignItems: "center", justifyContent: "center",
                backdropFilter: "blur(10px)",
              }}
            >
              <Box component="span" sx={{ fontSize: 20 }}>✦</Box>
            </Box>
            <Typography
              sx={{ color: "white", fontFamily: "'Manrope', sans-serif", fontWeight: 700, fontSize: "1.1rem", letterSpacing: "-0.01em" }}
            >
              ClinicOS
            </Typography>
          </Box>

          <Typography
            variant="h2"
            sx={{
              color: "white",
              fontFamily: "'Manrope', sans-serif",
              fontWeight: 800,
              fontSize: { md: "2.8rem", lg: "3.2rem" },
              lineHeight: 1.1,
              letterSpacing: "-0.03em",
              mb: 3,
            }}
          >
            Your health,<br />
            <Box component="span" sx={{ color: "#7ec8a0" }}>beautifully</Box>
            <br />managed.
          </Typography>

          <Typography
            sx={{
              color: "rgba(255,255,255,0.65)",
              fontSize: "1rem",
              lineHeight: 1.7,
              maxWidth: 320,
              mb: 6,
            }}
          >
            Join thousands of patients who manage their appointments, prescriptions, and health records in one calm, elegant space.
          </Typography>

          {/* Step indicators */}
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            {steps.map((label, i) => (
              <Box key={i} sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                <Box
                  sx={{
                    width: 28, height: 28, borderRadius: "50%",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    background: i < step
                      ? "#006d3c"
                      : i === step
                      ? "rgba(255,255,255,0.2)"
                      : "rgba(255,255,255,0.06)",
                    border: i === step ? "2px solid rgba(255,255,255,0.4)" : "none",
                    transition: "all 0.3s ease",
                    fontSize: "0.7rem",
                    color: "white",
                    fontWeight: 700,
                  }}
                >
                  {i < step ? "✓" : i + 1}
                </Box>
                <Typography
                  sx={{
                    color: i === step ? "white" : "rgba(255,255,255,0.4)",
                    fontFamily: "'Manrope', sans-serif",
                    fontWeight: i === step ? 600 : 400,
                    fontSize: "0.9rem",
                    transition: "all 0.3s ease",
                  }}
                >
                  {label}
                </Typography>
              </Box>
            ))}
          </Box>
        </Box>
      </Box>

      {/* ── Right panel (form) ── */}
      <Box
        sx={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          px: { xs: 3, sm: 6, md: 8 },
          py: 6,
          overflowY: "auto",
        }}
      >
        {/* Progress bar */}
        <Box sx={{ width: "100%", maxWidth: 480, mb: 4 }}>
          <LinearProgress
            variant="determinate"
            value={progress}
            sx={{
              height: 3,
              borderRadius: 2,
              backgroundColor: "rgba(0,83,148,0.1)",
              "& .MuiLinearProgress-bar": {
                backgroundColor: "#005394",
                borderRadius: 2,
              },
            }}
          />
        </Box>

        <Box sx={{ width: "100%", maxWidth: 480 }}>
          {/* ───── STEP 0: Registration form ───── */}
          {step === 0 && (
            <Box component="form" onSubmit={handleRegisterSubmit} noValidate>
              <Typography
                variant="h4"
                sx={{
                  fontFamily: "'Manrope', sans-serif",
                  fontWeight: 800,
                  color: "#111827",
                  letterSpacing: "-0.025em",
                  mb: 0.5,
                }}
              >
                Create your account
              </Typography>
              <Typography sx={{ color: "#6b7280", fontSize: "0.95rem", mb: 4 }}>
                Already have one?{" "}
                <Link to="/login" style={{ color: "#005394", fontWeight: 600, textDecoration: "none" }}>
                  Sign in →
                </Link>
              </Typography>

              {error && (
                <Alert severity="error" sx={{ mb: 3, borderRadius: 2 }} onClose={clearError}>
                  {error}
                </Alert>
              )}

              <Box sx={{ display: "flex", flexDirection: "column", gap: 2.5 }}>
                {/* Full Name */}
                <TextField
                  name="fullName"
                  label="Full Name"
                  value={form.fullName}
                  onChange={handleFormChange}
                  error={!!formErrors.fullName}
                  helperText={formErrors.fullName}
                  fullWidth
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <PersonOutlined sx={{ color: "#9ca3af", fontSize: 20 }} />
                      </InputAdornment>
                    ),
                  }}
                />

                {/* Email */}
                <TextField
                  name="email"
                  label="Email Address"
                  type="email"
                  value={form.email}
                  onChange={handleFormChange}
                  error={!!formErrors.email}
                  helperText={formErrors.email}
                  fullWidth
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <EmailOutlined sx={{ color: "#9ca3af", fontSize: 20 }} />
                      </InputAdornment>
                    ),
                  }}
                />

                {/* Gender + Date of Birth side by side */}
                <Box sx={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 2 }}>
                  <TextField
                    name="gender"
                    label="Gender"
                    select
                    value={form.gender}
                    onChange={handleFormChange}
                    error={!!formErrors.gender}
                    helperText={formErrors.gender}
                  >
                    {GENDERS.map((g) => (
                      <MenuItem key={g} value={g}>{g}</MenuItem>
                    ))}
                  </TextField>

                  <TextField
                    name="dateOfBirth"
                    label="Date of Birth"
                    type="date"
                    value={form.dateOfBirth}
                    onChange={handleFormChange}
                    error={!!formErrors.dateOfBirth}
                    helperText={formErrors.dateOfBirth}
                    InputLabelProps={{ shrink: true }}
                  />
                </Box>

                {/* Mobile */}
                <TextField
                  name="mobileNo"
                  label="Mobile Number"
                  value={form.mobileNo}
                  onChange={handleFormChange}
                  error={!!formErrors.mobileNo}
                  helperText={formErrors.mobileNo}
                  placeholder="+94771234567"
                  fullWidth
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <PhoneOutlined sx={{ color: "#9ca3af", fontSize: 20 }} />
                      </InputAdornment>
                    ),
                  }}
                />

                {/* Password */}
                <TextField
                  name="password"
                  label="Password"
                  type={showPassword ? "text" : "password"}
                  value={form.password}
                  onChange={handleFormChange}
                  error={!!formErrors.password}
                  helperText={formErrors.password || "Minimum 8 characters"}
                  fullWidth
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <LockOutlined sx={{ color: "#9ca3af", fontSize: 20 }} />
                      </InputAdornment>
                    ),
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton onClick={() => setShowPassword((v) => !v)} edge="end" size="small">
                          {showPassword ? <VisibilityOff sx={{ fontSize: 18 }} /> : <Visibility sx={{ fontSize: 18 }} />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />

                {/* Confirm Password */}
                <TextField
                  name="confirmPassword"
                  label="Confirm Password"
                  type={showConfirm ? "text" : "password"}
                  value={form.confirmPassword}
                  onChange={handleFormChange}
                  error={!!formErrors.confirmPassword}
                  helperText={formErrors.confirmPassword}
                  fullWidth
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <LockOutlined sx={{ color: "#9ca3af", fontSize: 20 }} />
                      </InputAdornment>
                    ),
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton onClick={() => setShowConfirm((v) => !v)} edge="end" size="small">
                          {showConfirm ? <VisibilityOff sx={{ fontSize: 18 }} /> : <Visibility sx={{ fontSize: 18 }} />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />

                <Button
                  type="submit"
                  variant="contained"
                  fullWidth
                  disabled={loading}
                  sx={primaryBtnSx}
                >
                  {loading ? <CircularProgress size={22} sx={{ color: "white" }} /> : "Create Account →"}
                </Button>
              </Box>
            </Box>
          )}

          {/* ───── STEP 1: OTP verification ───── */}
          {step === 1 && (
            <Box component="form" onSubmit={handleOtpSubmit} noValidate>
              <Typography
                variant="h4"
                sx={{
                  fontFamily: "'Manrope', sans-serif",
                  fontWeight: 800,
                  color: "#111827",
                  letterSpacing: "-0.025em",
                  mb: 0.5,
                }}
              >
                Check your inbox
              </Typography>
              <Typography sx={{ color: "#6b7280", fontSize: "0.95rem", mb: 1 }}>
                We sent a 6-digit code to
              </Typography>
              <Typography sx={{ color: "#005394", fontWeight: 700, fontSize: "0.95rem", mb: 4 }}>
                {email}
              </Typography>

              {error && (
                <Alert severity="error" sx={{ mb: 3, borderRadius: 2 }} onClose={clearError}>
                  {error}
                </Alert>
              )}

              {/* OTP boxes */}
              <Box sx={{ display: "flex", gap: 1.5, justifyContent: "center", mb: 4 }}>
                {otp.map((digit, index) => (
                  <Box
                    key={index}
                    component="input"
                    ref={(el) => (otpRefs.current[index] = el)}
                    type="text"
                    inputMode="numeric"
                    maxLength={1}
                    value={digit}
                    onChange={(e) => handleOtpChange(index, e.target.value)}
                    onKeyDown={(e) => handleOtpKeyDown(index, e)}
                    onPaste={index === 0 ? handleOtpPaste : undefined}
                    sx={{
                      width: 52,
                      height: 60,
                      textAlign: "center",
                      fontSize: "1.5rem",
                      fontWeight: 700,
                      fontFamily: "'Manrope', sans-serif",
                      border: digit ? "2px solid #005394" : "2px solid #e5e7eb",
                      borderRadius: "12px",
                      background: digit ? "#f0f7ff" : "#f9fafb",
                      color: "#005394",
                      outline: "none",
                      transition: "all 0.2s ease",
                      cursor: "text",
                      "&:focus": {
                        borderColor: "#005394",
                        background: "#f0f7ff",
                        boxShadow: "0 0 0 3px rgba(0,83,148,0.12)",
                      },
                    }}
                  />
                ))}
              </Box>

              <Button
                type="submit"
                variant="contained"
                fullWidth
                disabled={loading || otp.join("").length < OTP_LENGTH}
                sx={{ ...primaryBtnSx, mb: 3 }}
              >
                {loading ? <CircularProgress size={22} sx={{ color: "white" }} /> : "Verify & Continue →"}
              </Button>

              {/* Resend */}
              <Box sx={{ textAlign: "center" }}>
                <Typography sx={{ color: "#6b7280", fontSize: "0.9rem" }}>
                  Didn't receive the code?{" "}
                  {canResend ? (
                    <Box
                      component="button"
                      type="button"
                      onClick={handleResend}
                      sx={{
                        background: "none", border: "none", cursor: "pointer",
                        color: "#005394", fontWeight: 700, fontSize: "0.9rem",
                        fontFamily: "inherit", p: 0,
                        "&:hover": { textDecoration: "underline" },
                      }}
                    >
                      Resend code
                    </Box>
                  ) : (
                    <Box component="span" sx={{ color: "#9ca3af" }}>
                      Resend in {countdown}s
                    </Box>
                  )}
                </Typography>
              </Box>

              <Box sx={{ mt: 3, textAlign: "center" }}>
                <Box
                  component="button"
                  type="button"
                  onClick={() => { setStep(0); clearError(); }}
                  sx={{
                    background: "none", border: "none", cursor: "pointer",
                    color: "#6b7280", fontSize: "0.85rem", fontFamily: "inherit",
                    "&:hover": { color: "#005394" },
                  }}
                >
                  ← Use a different email
                </Box>
              </Box>
            </Box>
          )}

          {/* ───── STEP 2: Success ───── */}
          {step === 2 && (
            <Box sx={{ textAlign: "center" }}>
              <Box
                sx={{
                  width: 80, height: 80, borderRadius: "50%",
                  background: "linear-gradient(135deg, #e8f5e9, #c8e6c9)",
                  display: "flex", alignItems: "center", justifyContent: "center",
                  mx: "auto", mb: 4,
                }}
              >
                <Box component="span" sx={{ fontSize: 44, color: "#006d3c", lineHeight: 1 }}>
                  ✓
                </Box>
              </Box>
              <Typography
                variant="h4"
                sx={{
                  fontFamily: "'Manrope', sans-serif",
                  fontWeight: 800,
                  color: "#111827",
                  letterSpacing: "-0.025em",
                  mb: 1.5,
                }}
              >
                You're all set!
              </Typography>
              <Typography sx={{ color: "#6b7280", lineHeight: 1.7, mb: 5 }}>
                Your account has been verified and you're now logged in.
                Welcome to ClinicOS.
              </Typography>
              {/* Navigation happens automatically via useAuth hook */}
              <CircularProgress size={28} sx={{ color: "#005394" }} />
              <Typography sx={{ color: "#9ca3af", fontSize: "0.85rem", mt: 1.5 }}>
                Redirecting to your dashboard…
              </Typography>
            </Box>
          )}
        </Box>
      </Box>
    </Box>
  );
}

const primaryBtnSx = {
  height: 52,
  borderRadius: "12px",
  background: "linear-gradient(135deg, #005394 0%, #003a6b 100%)",
  fontFamily: "'Manrope', sans-serif",
  fontWeight: 700,
  fontSize: "0.95rem",
  letterSpacing: "0.01em",
  textTransform: "none",
  boxShadow: "0 4px 20px rgba(0,83,148,0.25)",
  "&:hover": {
    background: "linear-gradient(135deg, #004280 0%, #002855 100%)",
    boxShadow: "0 6px 28px rgba(0,83,148,0.35)",
    transform: "translateY(-1px)",
  },
  "&:disabled": {
    background: "#e5e7eb",
    boxShadow: "none",
    transform: "none",
  },
  transition: "all 0.2s ease",
};