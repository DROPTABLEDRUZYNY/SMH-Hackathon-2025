"use client";

import { useRouter } from "next/navigation";
import { logout } from "@/services/authService";
import { Button } from "@/components/ui/button";

export default function LogoutButton({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await logout();
      console.log("Logged out!");
      router.push("/login");
    } catch (err) {
      console.error("Logout failed");
    }
  };

  return (
    <div onClick={handleLogout} className={className}>
      {children}
    </div>
  );
}
