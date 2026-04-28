import React from 'react'
import { Link } from "react-router-dom";
import { useState, useEffect, useRef } from 'react'
import { useLocation, useNavigate } from "react-router-dom";
import theme from '../../theme.js'
import { useAuth } from '../../hooks/useAuth.js';
import {
    Box,
    TextField,
    Button,
    Typography,
    Alert,
    CircularProgress,
} from '@mui/material'

const OTP_LENGTH = 6;
const OTP_RESEND_SECONDS = 60;


const OtpVerification = ({ email: propEmail }) => {
    const { verifyRegistrationOtp, resendRegistrationOtp, loading, error, clearError } = useAuth();
    const location = useLocation();
    const navigate = useNavigate();
    const [email] = useState(propEmail || location.state?.email || "");
    const [resendNonce, setResendNonce] = useState(0);

    const [otp, setOtp] = useState(Array(OTP_LENGTH).fill(""));
    const [countdown, setCountdown] = useState(OTP_RESEND_SECONDS);
    const [canResend, setCanResend] = useState(false);
    const otpRefs = useRef([]);


    useEffect(() => {
        if (!email) return;
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

    }, [email, resendNonce]);

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
        await verifyRegistrationOtp(email, code);
    };

    const handleResend = async () => {
        if (!canResend) return;
        const result = await resendRegistrationOtp(email);
        if (result.success) {
            setOtp(Array(OTP_LENGTH).fill(""));
            setResendNonce((value) => value + 1);
        }
    };


    return (
        <Box
            sx={{

                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                backgroundColor: "background.default",
                borderRadius: 2,
                padding: 3,
                margin: 5
            }}
        >
            {!email && (
                <Box sx={{ width: "100%", maxWidth: 560, mb: 2 }}>
                    <Alert severity="warning">
                        Missing registration email. Please register first.
                        <Button onClick={() => navigate("/register")} sx={{ ml: 2 }}>
                            Back to Register
                        </Button>
                    </Alert>
                </Box>
            )}

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
                                    background:"#f0f7ff" ,
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
        </Box>
    )
}

export default OtpVerification