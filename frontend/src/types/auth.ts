export interface User {
    user_id: string;
    full_name: string;
    email: string;
    gender: "male" | "female" | "other";
    date_of_birth: string | null;
    mobile_no: string;
    profile_image_url?: string | null;
    user_type: string;
    sub?: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

export interface RegisterResponse {
  message: string;
  user_metadata?: Record<string, unknown>;
}

export interface RegisterPayload {
    full_name: string;
    email: string;
    password: string;
    gender: "male" | "female" | "other";
    date_of_birth: string;
    mobile_no: string;
    profile_image_url?: string;
    user_type?: string;
}

export interface LoginPayload {
    email: string;
    password: string;
}

export interface GuestUser {
  full_name: string;
  gender: "male" | "female" | "other";
  age: number;
}

export interface GuestUserResponse {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
  user: User;
}
