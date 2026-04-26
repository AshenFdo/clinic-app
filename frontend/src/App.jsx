import './App.css'
import React from 'react'
import { Navigate, Route, Routes } from "react-router-dom";
import Register_sample from "./pages/auth/Register_sample";
import RegisterForm from "./components/auth/RegisterForm";
import OtpVerification from './components/auth/OtpVerification';
import UserSample from './pages/auth/user_sample';
import LoginForm from './components/auth/LoginForm';
import ForgetPassword from './components/auth/ForgetPassword';

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/register" replace />} />
      <Route path="/register" element={<RegisterForm />} />
      <Route path="/register-sample" element={<Register_sample />} />
      <Route path="/login" element={<LoginForm />} />
      <Route path="/otp" element={<OtpVerification />} />
      <Route path="/user_sample" element={<UserSample />} />
      <Route path="/forgot-password" element={<ForgetPassword />} />
      
      <Route path="*" element={<Navigate to="/register" replace />} />
    </Routes>

  )
}

export default App