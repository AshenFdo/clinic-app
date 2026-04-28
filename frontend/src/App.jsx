import './App.css'
import React from 'react'
import { Navigate, Route, Routes } from "react-router-dom";
import RegisterPage from './pages/auth/RegisterPage';
import OtpVerification from './components/auth/OtpVerification';
import UserSample from './pages/auth/user_sample';
import LoginForm from './components/auth/LoginForm';
import ForgetPassword from './components/auth/ForgetPassword';
import LandingPage from './pages/auth/LandingPage';

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/landing" replace />} />
      <Route path="/landing" element={<LandingPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/login" element={<LoginForm />} />
      <Route path="/otp" element={<OtpVerification />} />
      <Route path="/user_sample" element={<UserSample />} />
      <Route path="/forgot-password" element={<ForgetPassword />} />
      
      <Route path="*" element={<Navigate to="/register" replace />} />
    </Routes>

  )
}

export default App