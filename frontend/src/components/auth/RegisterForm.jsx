import React from 'react'
import { useState, useEffect, useRef } from 'react'
import { Link, useNavigate } from "react-router-dom";
import theme from '../../theme.js'
import { useAuth } from '../../hooks/useAuth.js';
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
    FormControl,
    InputLabel,
    OutlinedInput,
    FormHelperText,


} from '@mui/material'
import {
    Visibility,
    VisibilityOff,
    PersonOutlined,
    EmailOutlined,
    PhoneOutlined,
    LockOutlined,
} from "@mui/icons-material";


const RegisterForm = () => {
    const { register, loading, error, clearError } = useAuth();
    const navigate = useNavigate();
    const GENDERS = ["Male", "Female", "Other"];

    const [form, setForm] = useState({
        fullName: "",
        email: "",
        password: "",
        confirmPassword: "",
        gender: "",
        mobileNo: "",
        dateOfBirth: "",
    });

    /* Password visibility toggle */
    const [showPassword, setShowPassword] = React.useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = React.useState(false);

    const handleClickShowConfirmPassword = () => setShowConfirmPassword((show) => !show);
    const handleClickShowPassword = () => setShowPassword((show) => !show);

    const handleMouseDownPassword = (event) => {
        event.preventDefault();
    };
    const handleMouseUpPassword = (event) => {
        event.preventDefault();
    };

    const handleMouseDownConfirmPassword = (event) => {
        event.preventDefault();
    }
    const handleMouseUpConfirmPassword = (event) => {
        event.preventDefault();
    }


    const [formErrors, setFormErrors] = useState({});
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
            navigate("/otp", { state: { email: form.email } });
        }else {
            window.alert(result.error || "Registration failed. Please try again.");
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
            <Box component="form" onSubmit={handleRegisterSubmit} sx={{
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
                    Create your account
                </Typography>

                <Typography sx={{ color: theme.palette.text.secondary, mb: 3, font: theme.typography.body2 }}>
                    Already have one?{" "}
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

                <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>

                    {/* Name Field */}
                    <TextField
                        name="fullName"
                        label="Full Name"
                        value={form.fullName}
                        onChange={handleFormChange}
                        error={!!formErrors.fullName}
                        helperText={formErrors.fullName || ''}
                        fullWidth
                        InputProps={{
                            startAdornment: (
                                <InputAdornment position="start">
                                    <PersonOutlined sx={{ color: "action.active" }} />
                                </InputAdornment>
                            )
                        }} />

                    {/* Email Field */}
                    <TextField
                        name="email"
                        label="Email Address"
                        value={form.email}
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
                        }} />


                    {/* Gender + Date of Birth side by side */}
                    <Box sx={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 2 }}>
                        <TextField
                            name="gender"
                            label="Gender"
                            select
                            value={form.gender}
                            onChange={handleFormChange}
                            error={!!formErrors.gender}
                            helperText={formErrors.gender || ''}
                        >
                            {GENDERS.map((option) => (
                                <MenuItem key={option} value={option}>
                                    {option}
                                </MenuItem>
                            ))}

                        </TextField>
                        <TextField
                            name="dateOfBirth"
                            label="Date of Birth"
                            type="date"
                            value={form.dateOfBirth || ""}
                            onChange={handleFormChange}
                            error={!!formErrors.dateOfBirth}
                            helperText={formErrors.dateOfBirth || ''}
                            slotProps={{
                                inputLabel: { shrink: true },
                                input: { notched: true },
                            }}
                        />


                    </Box>

                    {/* Mobile Number Field */}
                    <TextField
                        name="mobileNo"
                        label="Mobile Number"
                        value={form.mobileNo}
                        onChange={handleFormChange}
                        error={!!formErrors.mobileNo}
                        helperText={formErrors.mobileNo || ''}
                        type="tel"
                        fullWidth
                        InputProps={{
                            startAdornment: (
                                <InputAdornment position="start">
                                    <PhoneOutlined sx={{ color: "action.active" }} />
                                </InputAdornment>
                            )
                        }} />

                    {/* Password Field */}
                    <FormControl fullWidth>
                        <InputLabel htmlFor="outlined-adornment-password">Password</InputLabel>
                        <OutlinedInput
                            name='password'
                            id="outlined-adornment-password"
                            type={showPassword ? 'text' : 'password'}
                            label="Password"
                            value={form.password}
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
                            Minimum 8 characters
                        </FormHelperText>
                    </FormControl>

                    {/* Confirm Password Field */}
                    <FormControl fullWidth>
                        <InputLabel htmlFor="outlined-adornment-confirm-password">Confirm Password</InputLabel>
                        <OutlinedInput
                            name='confirmPassword'
                            id="outlined-adornment-confirm-password"
                            type={showConfirmPassword ? 'text' : 'password'}
                            label="Confirm Password"
                            value={form.confirmPassword}
                            onChange={handleFormChange}
                            error={!!formErrors.confirmPassword}
                            aria-describedby="outlined-adornment-confirm-password-helper-text"
                            endAdornment={
                                <InputAdornment position="end">
                                    <IconButton
                                        aria-label={
                                            showConfirmPassword ? 'hide the password' : 'display the password'
                                        }
                                        onClick={handleClickShowConfirmPassword}
                                        onMouseDown={handleMouseDownConfirmPassword}
                                        onMouseUp={handleMouseUpConfirmPassword}
                                        edge="end"
                                    >
                                        {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                                    </IconButton>
                                </InputAdornment>
                            }
                        />
                        <FormHelperText id="outlined-adornment-confirm-password-helper-text">
                            Must match the password above
                        </FormHelperText>
                    </FormControl>


                    {/*Submit Button  */}
                    <Button
                        variant="contained"
                        color="primary"
                        type='submit'
                        fullWidth
                        sx={theme.components.MuiButton.styleOverrides.containedPrimary}
                        disabled={loading}
                    >
                        {loading ? <CircularProgress size={24} color='primary'/> : "Create New Account"}
                    </Button>

                </Box>

            </Box>

        </Box >




    )
}

export default RegisterForm;
