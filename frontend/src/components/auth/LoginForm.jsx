import React, { useState } from 'react'
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




const LoginForm = () => {
    const { loading, loginWithCredentials, error, clearError } = useAuth();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [formErrors, setFormErrors] = useState({});

    const [showPassword, setShowPassword] = useState(false);

    const handleClickShowPassword = () => setShowPassword((show) => !show);

    const handleMouseDownPassword = (event) => {
        event.preventDefault();
    };
    const handleMouseUpPassword = (event) => {
        event.preventDefault();
    };

    const validationForm = () => {
        const errors = {};
        if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) errors.email = "Valid email required";
        if (password.length < 8) errors.password = "Password must be at least 8 characters";
        return errors;
    }
    const handleFormChange = (e) => {
        const { name, value } = e.target;
        if (name === "email") setEmail(value);
        if (name === "password") setPassword(value);
        if (formErrors[name]) setFormErrors((prev) => ({ ...prev, [name]: "" }));
        clearError();
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        const errors = validationForm();
        if (Object.keys(errors).length) { setFormErrors(errors); return; }

        const result = await loginWithCredentials(email, password);

        // if (!result.success) {
        //     window.alert(result.error || "Login failed. Please try again.");
        // }
    }


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
            <Box component="form" onSubmit={handleLogin} sx={{
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
                    Welcome back
                </Typography>

                <Typography sx={{ color: theme.palette.text.secondary, mb: 3, font: theme.typography.body2 }}>
                    Don't have an account?{" "}
                    <Link to="/register" style={{ color: theme.palette.primary.main, fontWeight: "bold", textDecoration: "none" }}>
                        Sign up →
                    </Link>
                </Typography>

                {/*Display error message */}
                {error && (
                    <Alert severity="error" onClose={clearError} sx={{ mb: 3 }}>
                        {error}
                    </Alert>
                )}

                <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
                    <TextField
                        name="email"
                        label="Email Address"
                        value={email}
                        onChange={handleFormChange}
                        error={!!formErrors.email}
                        helperText={formErrors.email || ''}
                        fullWidth
                        InputProps={{
                            startAdornment: (
                                <InputAdornment position="start">
                                    <EmailOutlined sx={{ color: "action.active" }} />
                                </InputAdornment>
                            )
                        }}
                    />

                    <FormControl fullWidth>
                        <InputLabel htmlFor="outlined-adornment-password">Password</InputLabel>
                        <OutlinedInput
                            name='password'
                            id="outlined-adornment-password"
                            type={showPassword ? 'text' : 'password'}
                            label="Password"
                            value={password}
                            onChange={handleFormChange}
                            error={!!formErrors.password}
                            aria-describedby="outlined-adornment-password-helper-text"
                            endAdornment={
                                <InputAdornment position="end">
                                    <IconButton
                                        aria-label={
                                            showPassword ? 'hide the password' : 'display the password'
                                        }
                                        onClick={handleClickShowPassword}
                                        onMouseDown={handleMouseDownPassword}
                                        onMouseUp={handleMouseUpPassword}
                                        edge="end"
                                    >
                                        {showPassword ? <VisibilityOff /> : <Visibility />}
                                    </IconButton>
                                </InputAdornment>
                            }
                        />
                        <FormHelperText id="outlined-adornment-password-helper-text">
                            {formErrors.password || "Minimum 8 characters"}
                        </FormHelperText>
                    </FormControl>


                    <Button type="submit" variant="contained" size="large" disabled={loading}>
                        {loading ? <CircularProgress size={24} color="inherit" /> : "Sign in"}
                    </Button>
                </Box>


                <Typography sx={{ color: theme.palette.text.secondary, mt: 2, font: theme.typography.body2 }}>
                    <Link to="/forgot-password" style={{ color: theme.palette.primary.main, fontWeight: "bold", textDecoration: "none" }}>
                        Forgot password?
                    </Link>
                </Typography>

            </Box>
        </Box>

    )
}

export default LoginForm