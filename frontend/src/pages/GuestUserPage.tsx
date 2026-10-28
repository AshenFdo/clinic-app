import GuestUserForm from "../components/auth/GuestUserForm";

export default function GuestUserPage() {
    return (
        <div className="flex min-h-[calc(100vh-4rem)] w-full items-center justify-center bg-background px-4 py-8 sm:px-6">
            <GuestUserForm />
        </div>
    );
}
