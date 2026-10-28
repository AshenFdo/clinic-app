import { api } from "./client";
import {
    type User,
    type GuestUser,
    type AuthResponse,
    type GuestUserResponse,
    type RegisterPayload,
    type LoginPayload,
    type RegisterResponse
} from "../types/auth.ts";
import { tokenStorage } from "../utils/tokenStorage";


export const authApi = {
    register: (data: RegisterPayload) => api.post<RegisterResponse>("/auth/register", data).then(r => r.data),
    login: (data: LoginPayload) => api.post<AuthResponse>("/auth/login", data).then(r => r.data),
    verifyOtp: (email: string, otp: string) => api.post<AuthResponse>("/auth/verify-otp", { email, otp }).then(r => r.data),
    resendOtp: (email: string) => api.post("/auth/resend-otp", { email }),
    refresh: () => {
        const refreshToken = tokenStorage.getRefresh();
        if (!refreshToken) throw new Error("No refresh token");
        return api.post<{ access_token: string; refresh_token: string }>(
            "/auth/refresh-token",
            { refresh_token: refreshToken },
        ).then(r => r.data);
    },
    logout: () => api.post("/auth/logout"),
    createGuest: (data:GuestUser) => api.post<GuestUserResponse>("/auth/create-guest-user", data).then(r => r.data),
    me: () => api.get<User>("/auth/current-user").then(r => r.data)
}