import { BrowserRouter, Routes, Route } from "react-router-dom";
import NavBar from "./components/layout/NavBar"
import { Doctors } from "./pages/Doctors"
import Home from "./pages/Home";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import OtpVerifyPage from "./pages/OtpVerifyPage";
import GuestUserPage from "./pages/GuestUserPage";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./routes/ProtectedRoute";



function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <NavBar />
        <main className="flex-1">
          <Routes>
            <Route element={<ProtectedRoute />}>
              <Route path="/" element={<Home />} />
              <Route path="/doctors" element={<Doctors />} />
            </Route>
            <Route path="/sign-in" element={<LoginPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/sign-up" element={<RegisterPage />} />
            <Route path="/otp-verify" element={<OtpVerifyPage />} />
            <Route path="/guest-login" element={<GuestUserPage />} />
          </Routes>
        </main>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
