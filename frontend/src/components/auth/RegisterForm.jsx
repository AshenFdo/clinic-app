import React from 'react'
import { useState, useEffect } from 'react'
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
} from "@mui/icons-material";


const RegisterForm = ({ onSuccess }) => {
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
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

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

    const normalizeForm = (payload) => ({
        ...payload,
        fullName: payload.fullName.trim(),
        email: payload.email.trim().toLowerCase(),
        mobileNo: payload.mobileNo.replace(/\s+/g, ""),
    });

    const validateForm = () => {
        const normalized = normalizeForm(form);
        const errs = {};
        if (!normalized.fullName) errs.fullName = "Full name is required";
        if (!normalized.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) errs.email = "Valid email required";
        if (form.password.length < 8) errs.password = "Password must be at least 8 characters";
        if (!form.confirmPassword) {
            errs.confirmPassword = "Please confirm your password";
        } else if (form.password !== form.confirmPassword) {
            errs.confirmPassword = "Passwords don't match";
        }
        if (!form.gender) errs.gender = "Select a gender";
        if (!normalized.mobileNo.match(/^\+?[0-9]{9,15}$/)) errs.mobileNo = "Valid phone number required";
        if (!form.dateOfBirth) {
            errs.dateOfBirth = "Date of birth required";
        } else if (form.dateOfBirth > new Date().toISOString().split("T")[0]) {
            errs.dateOfBirth = "Date of birth cannot be in the future";
        }
        return errs;
    };

    const handleRegisterSubmit = async (e) => {
        e.preventDefault();
        const errs = validateForm();
        if (Object.keys(errs).length) { setFormErrors(errs); return; }

        const normalized = normalizeForm(form);
        setForm(normalized);

        const result = await register(normalized);
        if (result.success) {
            if (onSuccess) {
                onSuccess(normalized.email);
            } else {
                navigate("/otp", { state: { email: normalized.email } });
            }
        }
    };

    return (




        <Box component="form" onSubmit={handleRegisterSubmit} sx={{
            border: `1px solid ${theme.palette.divider}`,
            backgroundColor: theme.palette.background.paper,
            maxWidth: 600,
            padding: 4,
            borderRadius: 2,
            display: "flex",
            flexDirection: "column",
            justifyItems: "left",
            width: "100%",
            height: "fit-content",
        }}>
            <Typography
                sx={{
                    color: theme.palette.text.primary,
                    fontFamily: theme.typography.fontFamily,
                    fontWeight: theme.typography.h4,
                    letterSpacing: "-0.02em",
                    mb: 2
                }}
            >
                Create your account
            </Typography>

            {/*Display error message */}
            {error && (
                <Alert severity="error" onClose={clearError} sx={{ mb: 3 }}>
                    {error}
                </Alert>
            )}

            {/* Form Fields */}

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
                <FormControl fullWidth error={!!formErrors.password}>
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
                        {formErrors.password || "Minimum 8 characters"}
                    </FormHelperText>
                </FormControl>

                {/* Confirm Password Field */}
                <FormControl fullWidth error={!!formErrors.confirmPassword}>
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
                        {formErrors.confirmPassword || "Must match the password above"}
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
                    {loading ? <CircularProgress size={24} color='inherit' /> : "Create New Account"}
                </Button>

            </Box>

        </Box>






    )
}

export default RegisterForm;
