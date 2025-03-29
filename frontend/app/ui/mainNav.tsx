"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { logout, userEmail$ } from "@/services/authService";
import { useRouter } from "next/navigation";

interface User {
  email: string;
}

export default function MainNav() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Subskrybuj się do zmian w stanie autentykacji
    const subscription = userEmail$.subscribe((email) => {
      if (email) {
        setUser({ email });
      } else {
        setUser(null);
      }
      setIsLoading(false);
    });

    // Cleanup subskrypcji
    return () => subscription.unsubscribe();
  }, []);

  const handleLogout = async () => {
    try {
      await logout();
      router.push('/');
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <nav className="bg-white/10 py-4 backdrop-blur-lg px-6 flex fixed top-5 left-5 right-5 z-50 rounded-lg justify-between items-center">
      <div className="flex items-center gap-4 bg-transparent">
        <Link href="/" className="text-white text-xl font-bold mr-6">
          Garbage Collector
        </Link>

        {user && (
          <>
            <Link href="/mark-trash">
              <Button
                variant="ghost"
                className="text-white hover:text-white hover:bg-white/10"
              >
                Mark trash
              </Button>
            </Link>
            <Link href="/collect-trash">
              <Button
                variant="ghost"
                className="text-white hover:text-white hover:bg-white/10"
              >
                Collect trash
              </Button>
            </Link>
          </>
        )}

        <Link href="/rankings">
          <Button
            variant="ghost"
            className="text-white hover:text-white hover:bg-white/10"
          >
            Rankings
          </Button>
        </Link>
      </div>

      <div className="bg-transparent">
        {isLoading ? (
          <div className="animate-pulse bg-gray-600 h-10 w-32 rounded"></div>
        ) : user ? (
          <div className="flex items-center bg-transparent">
            <div className="mr-4 text-right bg-transparent">
              <div className="text-white bg-transparent font-medium">
                {user.email}
              </div>
            </div>
            <Button
              onClick={handleLogout}
              variant="outline"
              className="border-white text-white hover:text-white bg-transparent hover:bg-white/25"
            >
              Log out
            </Button>
          </div>
        ) : (
          <Link href="/login">
            <Button
              variant="outline"
              className="border-white bg-transparent text-white hover:text-white hover:bg-white/20"
            >
              Log in
            </Button>
          </Link>
        )}
      </div>
    </nav>
  );
}
