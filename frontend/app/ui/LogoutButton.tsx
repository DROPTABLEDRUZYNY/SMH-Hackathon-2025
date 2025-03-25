"use client";

import { useRouter } from "next/navigation";
import { logout } from "@/services/authService";
import { Button } from "@/components/ui/button";

export default function LogoutButton() {
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
    <Button onClick={handleLogout} className="bg-red-600 text-white p-2 rounded">
      Logout
    </Button>
  );
}