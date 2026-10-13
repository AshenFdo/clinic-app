import LoginForm from "../components/auth/LoginForm";

export default function LoginPage() {
    return (
        <div className="flex min-h-[calc(100vh-4rem)] w-full items-center justify-center bg-background px-4 py-8 sm:px-6">
            <LoginForm />
        </div>
    )
}