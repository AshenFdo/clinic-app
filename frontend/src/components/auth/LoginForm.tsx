import Button from "../ui/Button"

import { useState } from "react";
import { useForm, type SubmitHandler } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Eye, EyeOff, LockKeyhole, Mail } from "lucide-react";
import { NavLink } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

// 1. Define the validation schema
const loginSchema = z.object({
    email: z.email("Please enter a valid email address"),
    password: z.string().min(6, "Password must be at least 6 characters"),
});

// 2. Infer the TypeScript type from the schema
type LoginFormData = z.infer<typeof loginSchema>;

export default function LoginForm() {
    const [serverError, setServerError] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    // 3. Configure React Hook Form
    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm<LoginFormData>({
        resolver: zodResolver(loginSchema),
        mode: "onBlur",
    });

    // 4. Handle form submission
    const onSubmit: SubmitHandler<LoginFormData> = async (data) => {
        setServerError("");

        try {
            await login(data);
            console.log("Login successful");
            navigate("/", { replace: true });
        } catch (error) {
            const message =
                typeof error === "object" &&
                error !== null &&
                "response" in error &&
                typeof error.response === "object" &&
                error.response !== null &&
                "data" in error.response &&
                typeof error.response.data === "object" &&
                error.response.data !== null &&
                "detail" in error.response.data &&
                typeof error.response.data.detail === "string"
                    ? error.response.data.detail
                    : "Unable to sign in. Please check your credentials and try again.";
            setServerError(message);
            console.error("Login error:", message, error);
        }
    };

    return (
        <div className="w-full max-w-md rounded-2xl border border-border-light bg-surface p-5 shadow-card sm:p-8">
            <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-6">
                <div className="text-center">
                    <div className="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-primary-light text-primary">
                        <LockKeyhole size={23} aria-hidden="true" />
                    </div>
                    <h1 className="text-2xl font-bold tracking-tight text-text-primary sm:text-3xl">
                        Welcome back
                    </h1>
                    <p className="mt-2 text-sm text-text-muted">
                        Sign in to your account
                    </p>
                </div>

                <div className="space-y-2">
                    <label
                        htmlFor="email"
                        className="block text-sm font-semibold text-text-secondary"
                    >
                        Email address
                    </label>
                    <div className="relative">
                        <Mail className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-text-muted" size={18} aria-hidden="true" />
                        <input
                            id="email"
                            type="email"
                            autoComplete="email"
                            placeholder="you@example.com"
                            aria-invalid={!!errors.email}
                            aria-describedby={errors.email ? "email-error" : undefined}
                            {...register("email")}
                            className="w-full rounded-lg border border-border bg-surface px-11 py-3 text-sm text-text-primary outline-none transition placeholder:text-text-disabled focus:border-border-focus focus:ring-4 focus:ring-primary-light"
                        />
                    </div>
                    {errors.email && (
                        <p id="email-error" role="alert" className="text-sm text-danger">
                            {errors.email.message}
                        </p>
                    )}
                </div>

                <div className="space-y-2">
                    <label
                        htmlFor="password"
                        className="block text-sm font-semibold text-text-secondary"
                    >
                        Password
                    </label>
                    <div className="relative">
                        <LockKeyhole className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-text-muted" size={18} aria-hidden="true" />
                        <input
                            id="password"
                            type={showPassword ? "text" : "password"}
                            autoComplete="current-password"
                            placeholder="Enter your password"
                            aria-invalid={!!errors.password}
                            aria-describedby={errors.password ? "password-error" : undefined}
                            {...register("password")}
                            className="w-full rounded-lg border border-border bg-surface px-11 py-3 pr-12 text-sm text-text-primary outline-none transition placeholder:text-text-disabled focus:border-border-focus focus:ring-4 focus:ring-primary-light"
                        />
                        <button
                            type="button"
                            onClick={() => setShowPassword((visible) => !visible)}
                            aria-label={showPassword ? "Hide password" : "Show password"}
                            className="absolute right-2 top-1/2 flex h-9 w-9 -translate-y-1/2 items-center justify-center rounded-md text-text-muted transition-colors hover:bg-surface-secondary hover:text-text-primary focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-border-focus"
                        >
                            {showPassword ? <EyeOff size={18} aria-hidden="true" /> : <Eye size={18} aria-hidden="true" />}
                        </button>
                    </div>
                    {errors.password && (
                        <p id="password-error" role="alert" className="text-sm text-danger">
                            {errors.password.message}
                        </p>
                    )}
                </div>

                <div className="flex items-center justify-between gap-4">
                    <NavLink to="/guest-login" className="text-sm font-semibold text-primary hover:text-primary-hover hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus">
                        Guest Login
                    </NavLink>
                    <NavLink to="/forgot-password" className="text-sm font-semibold text-primary hover:text-primary-hover hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus">
                        Forgot password?
                    </NavLink>
                </div>

                {serverError && <p role="alert" className="rounded-lg bg-danger-light px-3 py-2 text-sm text-danger">{serverError}</p>}

                <Button type="submit" disabled={isSubmitting}>
                    {isSubmitting ? "Signing in..." : "Sign in"}
                </Button>

                <p className="text-center text-sm text-text-muted">
                    Don't have an account?{" "}
                    <NavLink
                        to="/sign-up"
                        className="font-semibold text-primary hover:text-primary-hover hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus"
                    >
                        Sign up
                    </NavLink>
                </p>
            </form>
        </div>
    );
}
