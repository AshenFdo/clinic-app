import Button from "../ui/Button";

import { useState, type ReactNode } from "react";
import { useForm, type SubmitHandler } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { UserRound } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";


const guestUserSchema = z.object({
    full_name: z.string().trim().min(1, "Full name is required"),
    gender: z.enum(["male", "female", "other"], "Please select a valid gender"),
    age: z.number().int("Age must be a whole number").min(1, "Age must be at least 1").max(120, "Age must be 120 or less"),
});


type GuestUserFormValues = z.infer<typeof guestUserSchema>;
const inputClass = "w-full rounded-lg border border-border bg-surface px-11 py-3 text-sm text-text-primary outline-none transition placeholder:text-text-disabled focus:border-border-focus focus:ring-4 focus:ring-primary-light";

export default function GuestUserForm() {
    const [serverError, setServerError] = useState("");
    const { createGuestUser } = useAuth();
    const navigate = useNavigate();

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm<GuestUserFormValues>({
        resolver: zodResolver(guestUserSchema),
        mode: "onBlur",
    });

    const onSubmit: SubmitHandler<GuestUserFormValues> = async (data) => {
        setServerError("");

        try {
            await createGuestUser(data);
            navigate("/", { replace: true });
            console.log("Guest user created successfully", data);
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
                    : error instanceof Error
                        ? error.message
                        : "Unable to create a guest account. Please try again.";
            setServerError(message);
            console.error("Guest user creation error:", error);
        }
    }

    return (
        <div className="w-full max-w-2xl rounded-2xl border border-border-light bg-surface p-5 shadow-card sm:p-8">
            <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-6">
                <div className="text-center">
                    <div className="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-primary-light text-primary">
                        <UserRound size={23} aria-hidden="true" />
                    </div>
                    <h1 className="text-2xl font-bold tracking-tight text-text-primary sm:text-3xl">
                        Create Guest User
                    </h1>
                    <p className="mt-2 text-sm text-text-muted">
                        Fill in the details below to create a guest user account.
                    </p>
                </div>



                <div className="grid gap-5 sm:grid-cols-2">
                    <Field label="Full name" id="full_name" error={errors.full_name?.message} icon={<UserRound size={18} aria-hidden="true" />}>
                        <input id="full_name" autoComplete="name" placeholder="Your full name" aria-invalid={!!errors.full_name} aria-describedby={errors.full_name ? "full-name-error" : undefined} {...register("full_name")} className={inputClass} />
                    </Field>
                    <Field label="Gender" id="gender" error={errors.gender?.message} icon={<UserRound size={18} aria-hidden="true" />}>
                        <select
                            id="gender"
                            aria-invalid={!!errors.gender}
                            aria-describedby={errors.gender ? "gender-error" : undefined}
                            defaultValue=""
                            {...register("gender")}
                            className={`${inputClass} appearance-none`}
                        >
                            <option value="" disabled>Select your gender</option>
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                            <option value="other">Other</option>
                        </select>
                    </Field>
                    <Field label="Age" id="age" error={errors.age?.message} icon={<UserRound size={18} aria-hidden="true" />}>
                        <input id="age" type="number" min="1" max="120" placeholder="Your age" aria-invalid={!!errors.age} aria-describedby={errors.age ? "age-error" : undefined} {...register("age", { valueAsNumber: true })} className={inputClass} />
                    </Field>
                </div>

                {serverError && <p role="alert" className="rounded-lg bg-danger-light px-3 py-2 text-sm text-danger">{serverError}</p>}

                <Button type="submit" disabled={isSubmitting}>
                    {isSubmitting ? "Creating guest account..." : "Continue as guest"}
                </Button>
            </form>
        </div>
    );
}

function Field({ label, id, error, icon, children }: { label: string; id: string; error?: string; icon: ReactNode; children: ReactNode }) {
    return (
        <div className="space-y-2">
            <label htmlFor={id} className="block text-sm font-semibold text-text-secondary">{label}</label>
            <div className="relative">
                <span className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-text-muted">{icon}</span>
                {children}
            </div>
            {error && <p id={`${id === "full_name" ? "full-name" : id}-error`} role="alert" className="text-sm text-danger">{error}</p>}
        </div>
    );
}
