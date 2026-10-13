import { useEffect, useRef, useState, type ChangeEvent, type ClipboardEvent, type FormEvent, type KeyboardEvent } from "react";
import { ArrowLeft, KeyRound } from "lucide-react";
import { NavLink, useLocation, useNavigate } from "react-router-dom";
import Button from "../components/ui/Button";
import { useAuth } from "../hooks/useAuth";

const OTP_LENGTH = 6;
const RESEND_COOLDOWN_SECONDS = 30;

export default function OtpVerifyPage() {
    const [otp, setOtp] = useState<string[]>(Array(OTP_LENGTH).fill(""));
    const [secondsRemaining, setSecondsRemaining] = useState(RESEND_COOLDOWN_SECONDS);
    const inputRefs = useRef<Array<HTMLInputElement | null>>([]);
    const [serverError, setServerError] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);
    const location = useLocation();
    const navigate = useNavigate();
    const { verifyOtp, resendOtp } = useAuth();
    const email = (location.state as { email?: string } | null)?.email;

    useEffect(() => {
        if (secondsRemaining === 0) {
            return;
        }

        const timer = window.setInterval(() => {
            setSecondsRemaining((seconds) => Math.max(seconds - 1, 0));
        }, 1000);

        return () => window.clearInterval(timer);
    }, [secondsRemaining]);

    const focusInput = (index: number) => {
        inputRefs.current[index]?.focus();
    };

    const updateOtp = (index: number, value: string) => {
        const digit = value.replace(/\D/g, "").slice(-1);
        const nextOtp = [...otp];
        nextOtp[index] = digit;
        setOtp(nextOtp);

        if (digit && index < OTP_LENGTH - 1) {
            focusInput(index + 1);
        }
    };

    const handleChange = (index: number, event: ChangeEvent<HTMLInputElement>) => {
        updateOtp(index, event.target.value);
    };

    const handleKeyDown = (index: number, event: KeyboardEvent<HTMLInputElement>) => {
        if (event.key === "Backspace" && !otp[index] && index > 0) {
            const nextOtp = [...otp];
            nextOtp[index - 1] = "";
            setOtp(nextOtp);
            focusInput(index - 1);
        }

        if (event.key === "ArrowLeft" && index > 0) {
            focusInput(index - 1);
        }

        if (event.key === "ArrowRight" && index < OTP_LENGTH - 1) {
            focusInput(index + 1);
        }
    };

    const handlePaste = (event: ClipboardEvent<HTMLInputElement>) => {
        event.preventDefault();
        const pastedOtp = event.clipboardData.getData("text").replace(/\D/g, "").slice(0, OTP_LENGTH);
        if (!pastedOtp) {
            return;
        }

        setOtp(Array.from({ length: OTP_LENGTH }, (_, index) => pastedOtp[index] ?? ""));
        focusInput(Math.min(pastedOtp.length, OTP_LENGTH) - 1);
    };

    const handleResend = () => {
        if (!email) {
            setServerError("Your registration session has expired. Please register again.");
            return;
        }
        void resendOtp(email).then(() => {
            setSecondsRemaining(RESEND_COOLDOWN_SECONDS);
            setOtp(Array(OTP_LENGTH).fill(""));
            focusInput(0);
        }).catch(() => {
            setServerError("Unable to resend the verification code. Please try again.");
        });
    };

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setIsSubmitting(true);
        setServerError("");
        const otpValue = otp.join("");
        try {
            if (!email) {
                throw new Error("Your registration session has expired. Please register again.");
            }
            await verifyOtp(email, otpValue);
            navigate("/", { replace: true });
        } catch (error) {
            setServerError(error instanceof Error ? error.message : "Unable to verify the code. Please try again.");
        }finally{
            setIsSubmitting(false);
        }
    };

    const isComplete = otp.every(Boolean);

    return (
        <div className="flex min-h-[calc(100vh-4rem)] w-full items-center justify-center bg-background px-4 py-8 sm:px-6">
            <div className="w-full max-w-md rounded-2xl border border-border-light bg-surface p-5 shadow-card sm:p-8">
                <form onSubmit={handleSubmit} noValidate className="space-y-6">
                    <div className="text-center">
                        <div className="mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-primary-light text-primary">
                            <KeyRound size={23} aria-hidden="true" />
                        </div>
                        <h1 className="text-2xl font-bold tracking-tight text-text-primary sm:text-3xl">
                            Verify your account
                        </h1>
                        <p className="mt-2 text-sm leading-6 text-text-muted">
                            Enter the 6-digit code sent to your registered mobile number.
                        </p>
                    </div>

                    <div className="space-y-3">
                        <label className="block text-center text-sm font-semibold text-text-secondary">
                            Verification code
                        </label>
                        <div className="flex justify-center gap-2 sm:gap-3" role="group" aria-label="6-digit verification code">
                            {otp.map((digit, index) => (
                                <input
                                    key={index}
                                    ref={(element) => {
                                        inputRefs.current[index] = element;
                                    }}
                                    value={digit}
                                    onChange={(event) => handleChange(index, event)}
                                    onKeyDown={(event) => handleKeyDown(index, event)}
                                    onPaste={handlePaste}
                                    type="text"
                                    inputMode="numeric"
                                    autoComplete={index === 0 ? "one-time-code" : "off"}
                                    maxLength={1}
                                    aria-label={`Digit ${index + 1} of ${OTP_LENGTH}`}
                                    className="h-12 w-10 rounded-lg border border-border bg-surface text-center text-lg font-bold text-text-primary outline-none transition placeholder:text-text-disabled focus:border-border-focus focus:ring-4 focus:ring-primary-light sm:h-14 sm:w-12"
                                />
                            ))}
                        </div>
                    </div>
                    {serverError && (
                        <p role="alert" className="text-center text-sm text-danger">
                            {serverError}
                        </p>
                    )}
                    <Button type="submit" disabled={!isComplete || isSubmitting}>
                        {isSubmitting ? "Verifying..." : "Verify"}
                    </Button>

                    <div className="text-center text-sm text-text-muted">
                        <p>Didn't receive the code?</p>
                        <button
                            type="button"
                            onClick={handleResend}
                            disabled={secondsRemaining > 0}
                            className="mt-1 font-semibold text-primary transition-colors hover:text-primary-hover hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus disabled:cursor-not-allowed disabled:text-text-disabled disabled:no-underline"
                        >
                            {secondsRemaining > 0 ? `Resend code in 00:${secondsRemaining.toString().padStart(2, "0")}` : "Resend code"}
                        </button>
                    </div>

                    <NavLink
                        to="/sign-in"
                        className="flex items-center justify-center gap-2 text-sm font-semibold text-text-muted transition-colors hover:text-text-primary focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus"
                    >
                        <ArrowLeft size={16} aria-hidden="true" />
                        Back to sign in
                    </NavLink>
                </form>
            </div>
        </div>
    );
}