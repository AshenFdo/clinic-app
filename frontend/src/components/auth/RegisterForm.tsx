import { useEffect, useState, type ChangeEvent } from "react";
import { useForm, type SubmitHandler } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import {
    CalendarDays,
    Camera,
    Check,
    Eye,
    EyeOff,
    LockKeyhole,
    Mail,
    Phone,
    UserRound,
    X,
} from "lucide-react";
import { NavLink, useNavigate } from "react-router-dom";
import Button from "../ui/Button";
import { useAuth } from "../../hooks/useAuth";

const MINIMUM_AGE = 14;
const MAXIMUM_AGE = 120;

function parseDateInput(value: string): Date | undefined {
    const [year, month, day] = value.split("-").map(Number);
    const date = new Date(year, month - 1, day);

    return date.getFullYear() === year &&
        date.getMonth() === month - 1 &&
        date.getDate() === day
        ? date
        : undefined;
}

function formatDateInputValue(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
}

function shiftDateByYears(date: Date, years: number): Date {
    return new Date(date.getFullYear() + years, date.getMonth(), date.getDate());
}


const registerSchema = z.object({
    fullName: z.string().trim().min(2, "Please enter your full name"),
    email: z.email("Please enter a valid email address"),
    gender: z.enum(["male", "female", "other"], {
        error: "Please select your gender",
    }),
    date_of_birth: z
        .string()
        .min(1, "Please enter your date of birth")
        .refine((value) => Boolean(parseDateInput(value)), "Please enter a valid date of birth")
        .refine((value) => {
            const dateOfBirth = parseDateInput(value);
            const today = new Date();

            if (!dateOfBirth) return false;

            return dateOfBirth >= shiftDateByYears(today, -MAXIMUM_AGE) &&
                dateOfBirth <= shiftDateByYears(today, -MINIMUM_AGE);
        }, `You must be between ${MINIMUM_AGE} and ${MAXIMUM_AGE} years old to register`),
    mobileNumber: z
        .string()
        .regex(/^\d{10}$/, "Please enter a valid 10-digit mobile number"),
    profilePic: z
        .custom<FileList>()
        .optional()
        .refine(
            (files) =>
                !files ||
                files.length === 0 ||
                ["image/jpeg", "image/png", "image/webp"].includes(files[0].type),
            "Use a JPG, PNG, or WEBP image",
        )
        .refine(
            (files) => !files || files.length === 0 || files[0].size <= 2 * 1024 * 1024,
            "Profile picture must be smaller than 2 MB",
        ),
    password: z.string().min(6, "Password must be at least 6 characters"),
    confirmPassword: z.string().min(1, "Please confirm your password"),
}).refine((data) => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"],
});

type RegisterFormData = z.infer<typeof registerSchema>;

const inputClass =
    "w-full rounded-lg border border-border bg-surface px-11 py-3 text-sm text-text-primary outline-none transition placeholder:text-text-disabled focus:border-border-focus focus:ring-4 focus:ring-primary-light";

export default function RegisterForm() {
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
    const [profilePreview, setProfilePreview] = useState<string>();
    const [cropZoom, setCropZoom] = useState(1);
    const [cropX, setCropX] = useState(50);
    const [cropY, setCropY] = useState(50);
    const [isCropperOpen, setIsCropperOpen] = useState(false);
    const { register: registerUser } = useAuth();
    const navigate = useNavigate();
    const [serverError, setServerError] = useState("");

    const {
        register,
        handleSubmit,
        formState: { errors, isSubmitting },
    } = useForm<RegisterFormData>({
        resolver: zodResolver(registerSchema),
        mode: "onBlur",
    });

    useEffect(() => () => {
        if (profilePreview) URL.revokeObjectURL(profilePreview);
    }, [profilePreview]);

    const handleProfileChange = (event: ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (profilePreview) URL.revokeObjectURL(profilePreview);
        setCropZoom(1);
        setCropX(50);
        setCropY(50);
        setProfilePreview(file ? URL.createObjectURL(file) : undefined);
        setIsCropperOpen(Boolean(file));
    };

    const onSubmit: SubmitHandler<RegisterFormData> = async (data) => {
        try{
            await registerUser({
                full_name: data.fullName,
                email: data.email,
                date_of_birth: data.date_of_birth,
                mobile_no: data.mobileNumber,
                gender: data.gender,
                password: data.password,
            });
            navigate("/otp-verify", { state: { email: data.email }, replace: true });
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
                    : "Unable to create your account. Please try again.";
            setServerError(message);
        }
    };

    return (
        <div className="w-full max-w-2xl rounded-2xl border border-border-light bg-surface p-5 shadow-card sm:p-8">
            <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-6">
                <div className="text-center">
                    <div className="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-primary-light text-primary">
                        <UserRound size={23} aria-hidden="true" />
                    </div>
                    <h1 className="text-2xl font-bold tracking-tight text-text-primary sm:text-3xl">
                        Create your account
                    </h1>
                    <p className="mt-2 text-sm text-text-muted">
                        Join us to manage your healthcare journey
                    </p>
                </div>

                <div className="flex flex-col items-center gap-3 rounded-xl bg-surface-secondary p-4 sm:flex-row sm:text-left">
                    <button
                        type="button"
                        onClick={() => profilePreview && setIsCropperOpen(true)}
                        disabled={!profilePreview}
                        aria-label={profilePreview ? "Edit profile picture" : "No profile picture selected"}
                        className="flex h-24 w-24 shrink-0 items-center justify-center overflow-hidden rounded-full border-2 border-dashed border-border-focus bg-primary-light text-primary transition-opacity focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus enabled:hover:opacity-80 disabled:cursor-default"
                    >
                        {profilePreview ? (
                            <img
                                src={profilePreview}
                                alt="Profile preview"
                                className="h-full w-full object-cover"
                                style={{
                                    objectPosition: `${cropX}% ${cropY}%`,
                                    transform: `scale(${cropZoom})`,
                                }}
                            />
                        ) : (
                            <Camera size={26} aria-hidden="true" />
                        )}
                    </button>
                    <div className="text-center sm:text-left">
                        <label htmlFor="profilePic" className="inline-flex cursor-pointer items-center gap-2 rounded-lg border border-border px-3 py-2 text-sm font-semibold text-primary transition-colors hover:border-primary hover:bg-primary-light focus-within:outline-2 focus-within:outline-offset-2 focus-within:outline-border-focus">
                            <Camera size={16} aria-hidden="true" />
                            {profilePreview ? "Change picture" : "Upload picture"}
                            <input
                                id="profilePic"
                                type="file"
                                accept="image/png,image/jpeg,image/webp"
                                {...register("profilePic", { onChange: handleProfileChange })}
                                className="sr-only"
                            />
                        </label>
                        <p className="mt-1 text-xs text-text-muted">Optional · Square 1:1 crop · JPG, PNG or WEBP · Max 2 MB</p>
                        {errors.profilePic && <p role="alert" className="mt-1 text-sm text-danger">{errors.profilePic.message}</p>}
                    </div>
                </div>
                {isCropperOpen && profilePreview && (
                    <ProfileCropper
                        imageUrl={profilePreview}
                        zoom={cropZoom}
                        positionX={cropX}
                        positionY={cropY}
                        onZoomChange={setCropZoom}
                        onPositionXChange={setCropX}
                        onPositionYChange={setCropY}
                        onCancel={() => setIsCropperOpen(false)}
                        onConfirm={() => setIsCropperOpen(false)}
                    />
                )}
                {serverError && <p role="alert" className="rounded-lg bg-danger-light px-3 py-2 text-sm text-danger">{serverError}</p>}

                <div className="grid gap-5 sm:grid-cols-2">
                    <Field label="Full name" id="fullName" error={errors.fullName?.message} icon={<UserRound size={18} aria-hidden="true" />}>
                        <input id="fullName" autoComplete="name" placeholder="Your full name" aria-invalid={!!errors.fullName} {...register("fullName")} className={inputClass} />
                    </Field>
                    <Field label="Email address" id="email" error={errors.email?.message} icon={<Mail size={18} aria-hidden="true" />}>
                        <input id="email" type="email" autoComplete="email" placeholder="you@example.com" aria-invalid={!!errors.email} {...register("email")} className={inputClass} />
                    </Field>
                    <Field label="Gender" id="gender" error={errors.gender?.message} icon={<UserRound size={18} aria-hidden="true" />}>
                        <select
                            id="gender"
                            aria-invalid={!!errors.gender}
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
                    <Field label="Date of birth" id="date_of_birth" error={errors.date_of_birth?.message} icon={<CalendarDays size={18} aria-hidden="true" />}>
                        <input
                            id="date_of_birth"
                            type="date"
                            min={formatDateInputValue(shiftDateByYears(new Date(), -MAXIMUM_AGE))}
                            max={formatDateInputValue(shiftDateByYears(new Date(), -MINIMUM_AGE))}
                            autoComplete="bday"
                            aria-invalid={!!errors.date_of_birth}
                            {...register("date_of_birth")}
                            className={inputClass}
                        />
                    </Field>
                    <Field label="Mobile number" id="mobileNumber" error={errors.mobileNumber?.message} icon={<Phone size={18} aria-hidden="true" />}>
                        <input id="mobileNumber" type="tel" inputMode="numeric" autoComplete="tel" placeholder="07XXXXXXXX" aria-invalid={!!errors.mobileNumber} {...register("mobileNumber")} className={inputClass} />
                    </Field>
                </div>

                <div className="grid gap-5 sm:grid-cols-2">
                    <PasswordField id="password" label="Password" placeholder="At least 6 characters" visible={showPassword} setVisible={setShowPassword} error={errors.password?.message} register={register} />
                    <PasswordField id="confirmPassword" label="Confirm password" placeholder="Repeat your password" visible={showConfirmPassword} setVisible={setShowConfirmPassword} error={errors.confirmPassword?.message} register={register} />
                </div>

                <Button type="submit" disabled={isSubmitting}>
                    {isSubmitting ? "Creating account..." : "Create account"}
                </Button>

                <p className="text-center text-sm text-text-muted">
                    Already have an account?{" "}
                    <NavLink to="/sign-in" className="font-semibold text-primary hover:text-primary-hover hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus">
                        Sign in
                    </NavLink>
                </p>
            </form>
        </div>
    );
}

function Field({ label, id, error, icon, children }: { label: string; id: string; error?: string; icon: React.ReactNode; children: React.ReactNode }) {
    return (
        <div className="space-y-2">
            <label htmlFor={id} className="block text-sm font-semibold text-text-secondary">{label}</label>
            <div className="relative">
                <span className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-text-muted">{icon}</span>
                {children}
            </div>
            {error && <p role="alert" className="text-sm text-danger">{error}</p>}
        </div>
    );
}

function PasswordField({ id, label, placeholder, visible, setVisible, error, register }: {
    id: "password" | "confirmPassword";
    label: string;
    placeholder: string;
    visible: boolean;
    setVisible: (visible: boolean) => void;
    error?: string;
    register: ReturnType<typeof useForm<RegisterFormData>>["register"];
}) {
    return (
        <Field label={label} id={id} error={error} icon={<LockKeyhole size={18} aria-hidden="true" />}>
            <input id={id} type={visible ? "text" : "password"} autoComplete={id === "password" ? "new-password" : "new-password"} placeholder={placeholder} aria-invalid={!!error} {...register(id)} className={`${inputClass} pr-12`} />
            <button type="button" onClick={() => setVisible(!visible)} aria-label={visible ? `Hide ${label.toLowerCase()}` : `Show ${label.toLowerCase()}`} className="absolute right-2 top-1/2 flex h-9 w-9 -translate-y-1/2 items-center justify-center rounded-md text-text-muted hover:bg-surface-secondary hover:text-text-primary focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-border-focus">
                {visible ? <EyeOff size={18} aria-hidden="true" /> : <Eye size={18} aria-hidden="true" />}
            </button>
        </Field>
    );
}

function ProfileCropper({ imageUrl, zoom, positionX, positionY, onZoomChange, onPositionXChange, onPositionYChange, onCancel, onConfirm }: {
    imageUrl: string;
    zoom: number;
    positionX: number;
    positionY: number;
    onZoomChange: (value: number) => void;
    onPositionXChange: (value: number) => void;
    onPositionYChange: (value: number) => void;
    onCancel: () => void;
    onConfirm: () => void;
}) {
    return (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-slate-950/60 p-4 backdrop-blur-sm" role="dialog" aria-modal="true" aria-labelledby="crop-title">
            <div className="w-full max-w-md overflow-hidden rounded-2xl border border-border-light bg-surface shadow-dropdown">
                <div className="flex items-center justify-between border-b border-border-light px-5 py-4">
                    <div>
                        <h2 id="crop-title" className="font-semibold text-text-primary">Adjust profile picture</h2>
                        <p className="mt-1 text-xs text-text-muted">Position your photo inside the 1:1 frame.</p>
                    </div>
                    <button type="button" onClick={onCancel} aria-label="Close photo editor" className="flex h-9 w-9 items-center justify-center rounded-lg text-text-muted hover:bg-surface-secondary hover:text-text-primary focus-visible:outline-2 focus-visible:outline-border-focus">
                        <X size={19} aria-hidden="true" />
                    </button>
                </div>

                <div className="space-y-5 p-5">
                    <div className="mx-auto aspect-square w-full max-w-[280px] overflow-hidden rounded-xl bg-surface-secondary ring-1 ring-border">
                        <img
                            src={imageUrl}
                            alt="Profile crop preview"
                            className="h-full w-full object-cover"
                            style={{ objectPosition: `${positionX}% ${positionY}%`, transform: `scale(${zoom})` }}
                        />
                    </div>

                    <div className="space-y-4">
                        <CropControl label="Zoom" value={zoom} min={1} max={3} step={0.1} onChange={onZoomChange} display={`${zoom.toFixed(1)}x`} />
                        <CropControl label="Horizontal position" value={positionX} min={0} max={100} step={1} onChange={onPositionXChange} display={`${Math.round(positionX)}%`} />
                        <CropControl label="Vertical position" value={positionY} min={0} max={100} step={1} onChange={onPositionYChange} display={`${Math.round(positionY)}%`} />
                    </div>
                </div>

                <div className="flex flex-col-reverse gap-2 border-t border-border-light bg-surface-secondary px-5 py-4 sm:flex-row sm:justify-end">
                    <button type="button" onClick={onCancel} className="rounded-lg border border-border px-4 py-2.5 text-sm font-semibold text-text-secondary transition-colors hover:bg-surface hover:text-text-primary focus-visible:outline-2 focus-visible:outline-border-focus">
                        Cancel
                    </button>
                    <button type="button" onClick={onConfirm} className="inline-flex items-center justify-center gap-2 rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-primary-hover focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus">
                        <Check size={17} aria-hidden="true" />
                        Use this photo
                    </button>
                </div>
            </div>
        </div>
    );
}

function CropControl({ label, value, min, max, step, onChange, display }: {
    label: string;
    value: number;
    min: number;
    max: number;
    step: number;
    onChange: (value: number) => void;
    display: string;
}) {
    return (
        <label className="block text-sm font-medium text-text-secondary">
            <span className="mb-2 flex justify-between gap-2">
                <span>{label}</span>
                <span className="rounded-md bg-primary-light px-2 py-0.5 text-xs font-semibold text-primary">{display}</span>
            </span>
            <input type="range" min={min} max={max} step={step} value={value} onChange={(event) => onChange(Number(event.target.value))} className="w-full accent-primary" aria-label={label} />
        </label>
    );
}
