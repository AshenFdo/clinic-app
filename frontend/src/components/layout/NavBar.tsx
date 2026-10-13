import { useState } from "react";
import { Menu, Moon, Sun, X } from "lucide-react";
import { NavLink, useLocation } from "react-router-dom";
import useTheme from "../../hooks/useTheme";

type NavItem = {
	label: string;
	href: string;
};

const navItems: NavItem[] = [
	{ label: "Home", href: "/" },
	{ label: "Doctors", href: "/doctors" },
	{ label: "Emergency", href: "/emergency" },
	{ label: "Contact Us", href: "/contact" },
];

const authLinkClass = (isActive: boolean) =>
	`rounded-md px-4 py-2 text-sm font-semibold transition-all duration-200 ease-in-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus ${
		isActive
			? "bg-primary text-surface hover:bg-primary-hover"
			: "text-primary hover:bg-surface-tertiary"
	}`;

export function ThemeToggle() {
	const { theme, toggleTheme } = useTheme();
	const isDark = theme === "dark";

	return (
		<button
			type="button"
			onClick={toggleTheme}
			aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
			className="inline-flex h-10 w-10 items-center justify-center rounded-md text-text-secondary transition-colors hover:bg-surface-secondary hover:text-primary focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus"
		>
			{isDark ? <Sun size={19} aria-hidden="true" /> : <Moon size={19} aria-hidden="true" />}
		</button>
	);
}

export default function NavBar() {
	const [isMenuOpen, setIsMenuOpen] = useState(false);
	const { pathname } = useLocation();
	const isSignUpRoute = pathname.startsWith("/sign-up");

	const closeMenu = () => setIsMenuOpen(false);

	return (
		<nav className="sticky top-0 z-50 border-b border-border-light bg-surface/95 backdrop-blur transition-colors duration-300">
			<div className="mx-auto grid min-h-16 w-full max-w-7xl grid-cols-[1fr_auto] items-center gap-4 px-4 sm:px-6 lg:grid-cols-[1fr_auto_1fr] lg:px-8">
				<NavLink
					to="/"
					className="justify-self-start text-lg font-bold tracking-tight text-primary transition-colors hover:text-primary-hover focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-border-focus"
				>
					CompanyName
				</NavLink>

				<div className="hidden items-center gap-1 lg:flex">
					{navItems.map((item) => (
						<NavLink
							key={item.href}
							to={item.href}
							end={item.href === "/"}
							className={({ isActive }) =>
								`rounded-md px-3 py-2 text-sm font-medium transition-all duration-200 ease-in-out focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus ${isActive
									? "bg-primary-light text-primary"
									: "text-text-secondary hover:bg-surface-secondary hover:text-text-primary"
								}`
							}
						>
							{item.label}
						</NavLink>
					))}
				</div>

				<div className="hidden items-center justify-self-end gap-2 lg:flex">
					<ThemeToggle />
					<NavLink
						to="/sign-in"
						className={authLinkClass(!isSignUpRoute)}
					>
						Sign In
					</NavLink>
					<NavLink
						to="/sign-up"
						className={authLinkClass(isSignUpRoute)}
					>
						Sign Up
					</NavLink>
				</div>


				<button
					type="button"
					onClick={() => setIsMenuOpen((open) => !open)}
					aria-label={isMenuOpen ? "Close navigation menu" : "Open navigation menu"}
					aria-expanded={isMenuOpen}
					aria-controls="mobile-navigation"
					className="inline-flex h-10 w-10 items-center justify-center justify-self-end rounded-md text-text-secondary transition-colors hover:bg-surface-secondary hover:text-text-primary focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus lg:hidden"
				>
					{isMenuOpen ? <X size={22} aria-hidden="true" /> : <Menu size={22} aria-hidden="true" />}
				</button>
			</div>

			<div
				id="mobile-navigation"
				className={`${isMenuOpen ? "block" : "hidden"} border-t border-border-light bg-surface px-4 py-3 lg:hidden`}
			>
				<div className="flex flex-col gap-1">
					{navItems.map((item) => (
						<NavLink
							key={item.href}
							to={item.href}
							onClick={closeMenu}
							end={item.href === "/"}
							className={({ isActive }) =>
								`rounded-md px-3 py-2.5 text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-border-focus ${isActive
									? "bg-primary-light text-primary"
									: "text-text-secondary hover:bg-surface-secondary hover:text-text-primary"
								}`
							}
						>
							{item.label}
						</NavLink>
					))}
					<div className="mt-2 flex items-center justify-between border-t border-border-light pt-3">
						<ThemeToggle />
						<div className="flex gap-2">
							<NavLink
								to="/sign-in"
								onClick={closeMenu}
								className={authLinkClass(!isSignUpRoute)}
							>
								Sign In
							</NavLink>
							<NavLink
								to="/sign-up"
								onClick={closeMenu}
								className={authLinkClass(isSignUpRoute)}
							>
								Sign Up
							</NavLink>
						</div>

					</div>
				</div>
			</div>
		</nav>
	);
}
