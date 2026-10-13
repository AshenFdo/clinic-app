import { useState } from "react";
import Button from "../components/ui/Button"
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";

function Home () {
    const { user, logout } = useAuth();
    const [isloggingOut, setIsLoggingOut] = useState(false);
    const navigate = useNavigate();

    const handleLogout = async () => {
        setIsLoggingOut(true);  
        try {
            await logout();

            navigate("/login", { replace: true });
        } catch (error) {
            console.error("Logout failed:", error);
        } finally {
            setIsLoggingOut(false);
        }
    };

    return (
        <div className="flex h-max w-full flex-col items-center justify-center min-h-screen py-2 bg-background">
            <div className="flex flex-col items-center justify-center w-full flex-1 px-20 text-center">
                <h1>Home</h1>
                <p>Welcome, {user?.full_name}</p>
                <div className="mt-4 rounded-lg border border-border-light bg-surface p-4 text-left mb-5">
                    <p>Email: {user?.email}</p>
                    <p>User type: {user?.user_type}</p>
                    <p>User ID: {user?.user_id}</p>
                </div>
                <Button onClick={handleLogout} disabled={isloggingOut}>
                    {isloggingOut ? "Logging out..." : "Logout"}
                </Button>
            </div>
        </div>
    )
}

export default Home