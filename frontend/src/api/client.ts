import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";
import { tokenStorage } from "../utils/tokenStorage";

export const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use((config) => {
    const token = tokenStorage.getAccess();
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
});

let refreshPromise: Promise<string> | null = null;

api.interceptors.response.use(
    (res) => res,
    async (error: AxiosError) => {
        const original = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

        const isAuthCall = original.url?.includes("/auth/login") || original.url?.includes("/auth/refresh");
        if (error.response?.status === 401 && !original._retry && !isAuthCall) {
            original._retry = true;
            try {
                // share one refresh call if several requests fail at once
                refreshPromise ??= refreshAccessToken().finally(() => (refreshPromise = null));
                const newToken = await refreshPromise;
                original.headers.Authorization = `Bearer ${newToken}`;
                return api(original);
            } catch {
                tokenStorage.clear();
                window.location.href = "/login";
            }
        }
        return Promise.reject(error);
    }
);

async function refreshAccessToken(): Promise<string> {
    const refresh = tokenStorage.getRefresh();
    if (!refresh) throw new Error("No refresh token");
    // plain axios to avoid interceptor loops
    const { data } = await axios.post(`${import.meta.env.VITE_API_URL}/auth/refresh-token`, {
        refresh_token: refresh,
    });
    tokenStorage.set(data.access_token, data.refresh_token);
    return data.access_token;
}