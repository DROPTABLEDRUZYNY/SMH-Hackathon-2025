"use client";

import Link from "next/link";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import NavLinks from "@/app/ui/navLinks";
import SomeLogo from "@/app/ui/someLogo";
import { PowerIcon } from "@heroicons/react/24/outline";
import LogoutButton from "./LogoutButton";

// Тип для пользователя
interface User {
  firstName: string;
  lastName: string;
  email: string;
}

export default function MainNav() {
  // Состояние для отслеживания авторизации пользователя
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Имитация проверки авторизации пользователя
  useEffect(() => {
    // Здесь должен быть реальный запрос к API для проверки авторизации
    // Для примера используем localStorage
    const checkAuth = () => {
      const userData = localStorage.getItem("user");
      if (userData) {
        setUser(JSON.parse(userData));
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  // Функция для выхода из системы
  const handleLogout = () => {
    localStorage.removeItem("user");
    setUser(null);
  };

  return (
    <div className="flex h-full flex-col px-3 py-4 md:px-2">
      <Link
        className="mb-2 flex h-20 items-end justify-start rounded-xl bg-amber-500 p-4 md:h-40"
        href="/"
      >
        <div className="w-32 text-white md:w-40">
          <SomeLogo />
        </div>
      </Link>
      <div className="flex grow flex-row justify-between space-x-2 md:flex-col md:space-x-0 md:space-y-2">
        <NavLinks />
        <div className="hidden h-auto w-full grow rounded-xl bg-gray-50 md:block"></div>
        <form>
          {isLoading ? (
            <div className="animate-pulse bg-gray-600 h-10 w-32 rounded"></div>
          ) : user ? (
            <div className="flex items-center">
              <div className="mr-4 text-right">
                <div className="text-white font-medium">
                  {user.firstName} {user.lastName}
                </div>
                <div className="text-gray-300 text-sm">{user.email}</div>
              </div>
              <Button
                onClick={handleLogout}
                variant="outline"
                className="border-white text-white hover:bg-green-800"
              >
                Log out
              </Button>
            </div>
          ) : (
            <Button
              onClick={() => {
                // Для демонстрации создаем тестового пользователя
                const testUser = {
                  firstName: "Иван",
                  lastName: "Иванов",
                  email: "ivan@example.com",
                };
                localStorage.setItem("user", JSON.stringify(testUser));
                setUser(testUser);
              }}
              className="bg-green-500 hover:bg-green-600 text-white"
            >
              Log in
            </Button>
          )}
        </form>
      </div>
    </div>
  );
}
