import React from 'react'
import { useState, useEffect } from 'react';
import theme from '../../theme';
import RegisterForm from '../../components/auth/RegisterForm';
import OtpVerification from '../../components/auth/OtpVerification';
import LoginForm from '../../components/auth/LoginForm';
import Slide from '@mui/material/Slide';
// Add ForgetPassword import at the top
import ForgetPassword from '../../components/auth/ForgetPassword';

// Inside RegisterPage, add "forgot" to the authMode state handler
// and render it in the right panel:



import {
    Box,
    Typography,
    Button
} from '@mui/material'

const steps = ["Your Details", "Verify Email", "All Done"];


const RegisterPage = () => {
    const [authMode, setAuthMode] = useState(null); // null, "login", or "register"
    const [step, setStep] = useState(0); // 0: Add data, 1: Verify email with otp, 2: Success & upload profile picture
    const [userEmail, setUserEmail] = useState("");
    const [mounted, setMounted] = useState(false);


    useEffect(() => {
        setMounted(true);
    }, []);

    const handleRegistrationSuccess = (email) => {
        setUserEmail(email);
        setStep(1);
    };

    return (
        <>
            <Box sx={{
                height: "100vh",
                display: "flex",
                flexDirection: "row",
                background: "linear-gradient(160deg, #005394 0%, #003a6b 60%, #002244 100%)",
            }}>
                {/* Decorative circles */}
                {[
                    { size: 320, top: -80, left: 300, opacity: 0.08 },
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
                            border: `4px solid white`,
                            opacity: c.opacity,
                            top: c.top,
                            bottom: c.bottom,
                            left: c.left,
                            right: c.right,
                        }}
                    />
                ))}

                {/* Left side - Welcome message */}
                <Slide direction="up" in={mounted} timeout={500} appear>
                    <Box sx={{
                        display: { xs: "none", md: "flex" },
                        width: "40%",
                        flexDirection: "column",
                        justifyContent: "center",
                        alignItems: "flex-start",
                        position: "relative",
                        paddingLeft: 8,
                    }}>
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
                                    Suhada Clinic
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
                                    mb: 2,
                                }}
                            >
                                Join thousands of patients who manage their appointments, prescriptions, and health records in one calm, elegant space.
                            </Typography>
                        </Box>

                        <Box sx={{
                            position: "relative",
                            zIndex: 1,

                        }}>

                            <Box sx={{ display: "flex", gap: 2.5, flexDirection: "row" }}>
                                <Button
                                    onClick={() => {
                                        setAuthMode("login");
                                        setStep(0);
                                    }}
                                    sx={{
                                        padding: "14px 28px",
                                        fontSize: "1.1rem",
                                        fontWeight: 600,
                                        borderRadius: "12px",
                                        border: authMode === "login" ? "2px solid #7ec8a0" : "2px solid rgba(255,255,255,0.3)",
                                        color: authMode === "login" ? "#7ec8a0" : "rgba(255,255,255,0.8)",
                                        backgroundColor: authMode === "login" ? "rgba(126, 200, 160, 0.1)" : "transparent",
                                        backdropFilter: "blur(10px)",
                                        cursor: "pointer",
                                        transition: "all 0.3s ease",
                                        "&:hover": {
                                            backgroundColor: "rgba(126, 200, 160, 0.15)",
                                            border: "2px solid #7ec8a0",
                                            color: "#7ec8a0",
                                        }
                                    }}
                                >
                                    Login
                                </Button>
                                <Button
                                    onClick={() => {
                                        setAuthMode("register");
                                        setStep(0);
                                    }}
                                    sx={{
                                        padding: "14px 28px",
                                        fontSize: "1.1rem",
                                        fontWeight: 600,
                                        borderRadius: "12px",
                                        border: authMode === "register" ? "2px solid #7ec8a0" : "2px solid rgba(255,255,255,0.3)",
                                        color: authMode === "register" ? "#7ec8a0" : "rgba(255,255,255,0.8)",
                                        backgroundColor: authMode === "register" ? "rgba(126, 200, 160, 0.1)" : "transparent",
                                        backdropFilter: "blur(10px)",
                                        cursor: "pointer",
                                        transition: "all 0.3s ease",
                                        "&:hover": {
                                            backgroundColor: "rgba(126, 200, 160, 0.15)",
                                            border: "2px solid #7ec8a0",
                                            color: "#7ec8a0",
                                        }
                                    }}
                                >
                                    Register
                                </Button>
                            </Box>

                            {/* Step indicators */}
                            {(authMode === "register") && (
                                <Box sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 4 }}>
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
                            )}

                        </Box>

                    </Box>

                </Slide>
                {/* Right side - Registration form */}

                <Slide direction="up" in={mounted} timeout={900} appear>
                    <Box sx={{
                        width: { xs: "100%", md: "60%" },
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        justifyContent: "center",
                        padding: 4,
                        backgroundColor: null,
                        borderTopLeftRadius: 20,
                        borderBottomLeftRadius: 20,
                    }}>

                        {(authMode === "register" && step === 0) && <RegisterForm onSuccess={handleRegistrationSuccess} />}
                        {(authMode === "register" && step === 1) && <OtpVerification email={userEmail} />}
                    
                        {authMode === "login" && (
                            <LoginForm onForgotPassword={() => setAuthMode("forgot")} />
                        )}
                        {authMode === "forgot" && <ForgetPassword onBackToLogin={() => setAuthMode("login")} />}


                    </Box>
                </Slide>


            </Box>
        </>
    )
}

export default RegisterPage