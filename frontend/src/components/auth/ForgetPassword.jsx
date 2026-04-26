import React, { useState, useEffect, useRef } from 'react'
import { Link } from "react-router-dom";
import theme from '../../theme.js'
import { useAuth } from '../../hooks/useAuth.js';

import {
    Box,
    TextField,
    Button,
    Typography,
    InputAdornment,
    IconButton,
    Alert,
    FormControl,
    InputLabel,
    OutlinedInput,
    FormHelperText,
    CircularProgress,
} from '@mui/material'
import {
    Visibility,
    VisibilityOff,
    EmailOutlined,
} from "@mui/icons-material";

const OTP_LENGTH = 6;
const OTP_RESEND_SECONDS = 60;

const ForgetPassword = () => {
    const { loading, resetUserPassword, sendForgotPasswordOtp, verifyForgotPasswordOtp, error, clearError } = useAuth();
    const [email, setEmail] = useState("");
    const [emailError, setEmailError] = useState("");
    const [isStepTransitioning, setIsStepTransitioning] = useState(false);
    const [resendNonce, setResendNonce] = useState(0);
    const [recoverySession, setRecoverySession] = useState(null);

    const [otp, setOtp] = useState(Array(OTP_LENGTH).fill(""));
    const [countdown, setCountdown] = useState(OTP_RESEND_SECONDS);
    const [canResend, setCanResend] = useState(false);
    const otpRefs = useRef([]);
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [newPasswordError, setNewPasswordError] = useState("");
    const [confirmPasswordError, setConfirmPasswordError] = useState("");
    const [showNewPassword, setShowNewPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const [step, setStep] = useState(1); // 1: enter email, 2: enter OTP, 3: reset new password

    const validationEmail = () => {
        if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) return "Valid email required";
        return null;
    }

    const handleFormChange = (e) => {
        const { name, value } = e.target;
        if (name === "email") setEmail(value);
        if (emailError) setEmailError("");
        clearError();
    };


    const handleSendOTP = async (e) => {
        e.preventDefault();
        const emailError = validationEmail();
        if (emailError) { setEmailError(emailError); return; }
        setEmailError("");
        clearError();
        const result = await sendForgotPasswordOtp(email);
        if (result.success) {
            setIsStepTransitioning(true);
            setTimeout(() => {
                setStep(2);
                setIsStepTransitioning(false);
            }, 700);
        } else {
            window.alert(result.error || "Failed to send OTP. Please try again.");
        }
    }

    // Functions for OTP step (similar to OtpVerification.jsx)
    useEffect(() => {
        if (!email || step < 2) return;
        setCountdown(OTP_RESEND_SECONDS);
        setCanResend(false);

        const timer = setInterval(() => {
            setCountdown((prev) => {
                if (prev <= 1) {
                    setCanResend(true);
                    clearInterval(timer);
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);

        return () => clearInterval(timer);

    }, [email, resendNonce, step]);

    useEffect(() => {
        // Step 2 depends on a verified email context from step 1.
        if (step === 2 && !email) {
            setStep(1);
        }
    }, [step, email]);

    useEffect(() => {
        // Step 3 requires recovery session tokens from OTP verification.
        if (step === 3 && !recoverySession) {
            setStep(2);
        }
    }, [step, recoverySession]);


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
        clearError();
        const result = await verifyForgotPasswordOtp(email, code);
        if (result.success) {
            setRecoverySession(result.session);
            setStep(3);
        } else {
            window.alert(result.error || "OTP verification failed. Please try again.");
        }
    };

    const handleResend = async () => {
        if (!canResend) return;
        clearError();
        const result = await sendForgotPasswordOtp(email);
        if (result.success) {
            setOtp(Array(OTP_LENGTH).fill(""));
            setRecoverySession(null);
            setResendNonce((value) => value + 1);
        }
    };

    const handlePasswordSubmit = async (e) => {
        e.preventDefault();
        let hasError = false;

        if (newPassword.length < 8) {
            setNewPasswordError("Password must be at least 8 characters long");
            hasError = true;
        } else {
            setNewPasswordError("");
        }

        if (confirmPassword !== newPassword) {
            setConfirmPasswordError("Passwords do not match");
            hasError = true;
        } else {
            setConfirmPasswordError("");
        }

        if (!recoverySession?.access_token || !recoverySession?.refresh_token || hasError) return;

        const result = await resetUserPassword(
            recoverySession.access_token,
            recoverySession.refresh_token,
            newPassword,
            confirmPassword,
        );
        if (result.success) {
            
        } else {
            window.alert(result.error || "Failed to reset password. Please try again.");
        }
    };


    return (
        <Box
            sx={{
                minHeight: "100vh",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                backgroundColor: "background.default",
                padding: 3,
            }}
        >


            {step === 1 && (
                <>
                    <Box component="form" onSubmit={handleSendOTP} sx={{
                        border: `1px solid ${theme.palette.divider}`,
                        padding: 4,
                        borderRadius: 2,
                        display: "flex",
                        flexDirection: "column",
                        justifyItems: "left",
                        width: "100%",

                    }}>
                        <Typography
                            sx={{
                                color: theme.palette.text.primary,
                                fontFamily: theme.typography.fontFamily,
                                fontWeight: theme.typography.h4,
                                letterSpacing: "-0.02em",
                                mb: 0.5
                            }}
                        >
                            Enter your registered email
                        </Typography>

                        <Typography sx={{ color: theme.palette.text.secondary, mb: 3, font: theme.typography.body2 }}>
                            Remember your password?{" "}
                            <Link to="/login" style={{ color: theme.palette.primary.main, fontWeight: "bold", textDecoration: "none" }}>
                                Sign in →
                            </Link>
                        </Typography>
                        {/*Display error message */}
                        {error && (
                            <Alert severity="error" onClose={clearError} sx={{ mb: 3 }}>
                                {error}
                            </Alert>
                        )}


                        <Box sx={{ display: "flex", flexDirection: "column", gap: 4 }}>
                            <TextField
                                name="email"
                                label="Email Address"
                                value={email}
                                onChange={handleFormChange}
                                error={!!emailError}
                                helperText={emailError || ''}
                                fullWidth
                                InputProps={{
                                    startAdornment: (
                                        <InputAdornment position="start">
                                            <EmailOutlined sx={{ color: "action.active" }} />
                                        </InputAdornment>
                                    )
                                }}
                            />
                            <Button type="submit" variant="contained" size="large" disabled={loading || isStepTransitioning}>
                                {loading ? <CircularProgress size={24} color="inherit" /> : "Send OTP"}
                            </Button>

                            {isStepTransitioning && (
                                <Box sx={{ display: "flex", alignItems: "center", gap: 1.5 }}>
                                    <CircularProgress size={18} />
                                    <Typography variant="body2" sx={{ color: "text.secondary" }}>
                                        OTP sent. Opening verification step...
                                    </Typography>
                                </Box>
                            )}
                        </Box>
                    </Box>

                </>
            )
            }{step === 2 && (
                <>
                    <Box component="form" onSubmit={handleOtpSubmit} sx={{
                        border: `1px solid ${theme.palette.divider}`,
                        padding: 4,
                        borderRadius: 2,
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        gap: 3,

                        justifyContent: "center",
                        width: "100%",
                    }}>
                        <Typography sx={{
                            color: theme.palette.text.primary,
                            fontFamily: theme.typography.fontFamily,
                            fontSize: theme.typography.h3,
                            letterSpacing: "-0.02em",
                            mb: 0.5
                        }}>
                            Check your inbox
                        </Typography>
                        <Typography sx={{ color: theme.palette.text.secondary, mb: 3, font: theme.typography.body2 }}>
                            We sent a {`${OTP_LENGTH}-digit`} code to {email}
                        </Typography>

                        {/*Display Error Message */}
                        {error && (
                            <Typography sx={{ color: theme.palette.error.main, mb: 3, font: theme.typography.body2 }}>
                                {error}
                            </Typography>
                        )}

                        {/* OTP boxes */}
                        <Box sx={{
                            display: "flex",
                            gap: 1.5,
                            justifyContent: "center",
                            mb: 4
                        }}>
                            {otp.map((digit, index) => (
                                <TextField
                                    type="tel"
                                    autoComplete="one-time-code"
                                    key={index}
                                    inputProps={{
                                        inputMode: "numeric",
                                        maxLength: 1,
                                        style: {
                                            textAlign: "center",
                                            fontSize: theme.typography.h4,
                                            fontWeight: 800,
                                            fontFamily: theme.typography.fontFamily,
                                            lineHeight: "60px",
                                            padding: 0,
                                        },
                                    }}
                                    inputRef={(el) => (otpRefs.current[index] = el)}
                                    value={digit}
                                    onChange={(e) => handleOtpChange(index, e.target.value)}
                                    onKeyDown={(e) => handleOtpKeyDown(index, e)}
                                    onPaste={index === 0 ? handleOtpPaste : undefined}
                                    sx={{
                                        width: 52,
                                        height: 60,
                                        display: "flex",
                                        "& .MuiOutlinedInput-root": {
                                            height: 60,
                                            borderRadius: "12px",
                                            background: "#f0f7ff",
                                            color: theme.palette.primary.light,
                                            fontSize: theme.typography.h4,
                                            fontWeight: 800,
                                            fontFamily: theme.typography.fontFamily,
                                            transition: "all 0.2s ease",
                                            "& .MuiOutlinedInput-input": {
                                                height: "100%",
                                                boxSizing: "border-box",
                                                textAlign: "center",
                                                padding: 0,
                                                lineHeight: "60px",
                                            },
                                            "& fieldset": {
                                                border: digit ? "2px solid #005394" : "2px solid #e5e7eb",
                                            },
                                            "&:hover fieldset": {
                                                border: digit ? "2px solid #005394" : "2px solid #d1d5db",
                                            },
                                            "&.Mui-focused": {
                                                background: "#f0f7ff",
                                                boxShadow: "0 0 0 3px rgba(0,83,148,0.12)",
                                            },
                                            "&.Mui-focused fieldset": {
                                                border: "2px solid #005394",
                                            },
                                        },
                                    }}
                                />
                            ))}

                        </Box>

                        <Button
                            type='submit'
                            variant='contained'
                            fullWidth
                            disabled={loading || !email || otp.join("").length < OTP_LENGTH}
                            sx={theme.components.MuiButton.styleOverrides.containedPrimary}
                        >
                            {loading ? <CircularProgress size={22} sx={{ color: "white" }} /> : "Verify & Continue →"}
                        </Button>

                        <Typography sx={{ color: theme.palette.text.secondary, font: theme.typography.body2 }}>
                            {canResend ? "Didn't get the code?" : `Resend available in ${countdown}s`}
                        </Typography>
                        <Button
                            type='button'
                            onClick={handleResend}
                            disabled={!canResend || loading || !email}
                        >
                            Resend OTP
                        </Button>

                    </Box>
                </>
            )}

            {step === 3 && (
                <>
                    <Box component="form" onSubmit={handlePasswordSubmit} sx={{
                        border: `1px solid ${theme.palette.divider}`,
                        padding: 4,
                        borderRadius: 2,
                        display: "flex",
                        flexDirection: "column",
                        gap: 3,
                        width: "100%",
                    }}>
                        <Typography sx={{
                            color: theme.palette.text.primary,
                            fontFamily: theme.typography.fontFamily,
                            fontSize: theme.typography.h3,
                            letterSpacing: "-0.02em",
                            mb: 0.5
                        }}>
                            Reset your password
                        </Typography>
                        <Typography sx={{ color: theme.palette.text.secondary, mb: 1, font: theme.typography.body2 }}>
                            Enter a new password for {email}
                        </Typography>

                        {error && (
                            <Alert severity="error" onClose={clearError}>
                                {error}
                            </Alert>
                        )}

                        <FormControl fullWidth error={!!newPasswordError}>
                            <InputLabel htmlFor="new-password">New Password</InputLabel>
                            <OutlinedInput
                                id="new-password"
                                type={showNewPassword ? "text" : "password"}
                                value={newPassword}
                                onChange={(e) => {
                                    setNewPassword(e.target.value);
                                    if (newPasswordError) setNewPasswordError("");
                                    clearError();
                                }}
                                endAdornment={
                                    <InputAdornment position="end">
                                        <IconButton
                                            aria-label="toggle new password visibility"
                                            onClick={() => setShowNewPassword((value) => !value)}
                                            edge="end"
                                        >
                                            {showNewPassword ? <VisibilityOff /> : <Visibility />}
                                        </IconButton>
                                    </InputAdornment>
                                }
                                label="New Password"
                            />
                            {newPasswordError && <FormHelperText>{newPasswordError}</FormHelperText>}
                        </FormControl>

                        <FormControl fullWidth error={!!confirmPasswordError}>
                            <InputLabel htmlFor="confirm-password">Confirm Password</InputLabel>
                            <OutlinedInput
                                id="confirm-password"
                                type={showConfirmPassword ? "text" : "password"}
                                value={confirmPassword}
                                onChange={(e) => {
                                    setConfirmPassword(e.target.value);
                                    if (confirmPasswordError) setConfirmPasswordError("");
                                    clearError();
                                }}
                                endAdornment={
                                    <InputAdornment position="end">
                                        <IconButton
                                            aria-label="toggle confirm password visibility"
                                            onClick={() => setShowConfirmPassword((value) => !value)}
                                            edge="end"
                                        >
                                            {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                                        </IconButton>
                                    </InputAdornment>
                                }
                                label="Confirm Password"
                            />
                            {confirmPasswordError && <FormHelperText>{confirmPasswordError}</FormHelperText>}
                        </FormControl>

                        <Button
                            type='submit'
                            variant='contained'
                            fullWidth
                            disabled={
                                loading ||
                                !email ||
                                otp.join("").length < OTP_LENGTH ||
                                !newPassword ||
                                !confirmPassword
                            }
                            sx={theme.components.MuiButton.styleOverrides.containedPrimary}
                        >
                            {loading ? <CircularProgress size={22} sx={{ color: "white" }} /> : "Reset Password"}
                        </Button>
                    </Box>
                </>
            )}


        </Box>

    )
}

export default ForgetPassword