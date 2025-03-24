"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";

type LoginForm = {
  email: string;
  password: string;
};

async function getCsrfToken() {
    await fetch("http://localhost:8000/api/csrf/", {
      method: "GET",
      credentials: "include",
    });
  
    const csrfToken = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1];
  
    return csrfToken;
  }

export default function LoginPage() {
  const [error, setError] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>();
  
  const onSubmit = async (data: LoginForm) => {
    let csrfToken = await getCsrfToken();

    try {
      const res = await fetch("http://localhost:8000/api/users/auth/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json","X-CSRFToken": csrfToken || ""},
        body: JSON.stringify(data),
        credentials: "include", // Send cookies
      });

      if (!res.ok) throw new Error("Invalid credentials");
      console.log("Logged in!");
    } catch (err) {
      setError("Invalid email or password");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-4">Login</h1>
      {error && <p className="text-red-500">{error}</p>}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <input
          {...register("email", { required: "Email is required" })}
          type="email"
          placeholder="Email"
          className="w-full p-2 border border-gray-300 rounded"
        />
        {errors.email && <p className="text-red-500">{errors.email.message}</p>}

        <input
          {...register("password", { required: "Password is required" })}
          type="password"
          placeholder="Password"
          className="w-full p-2 border border-gray-300 rounded"
        />
        {errors.password && <p className="text-red-500">{errors.password.message}</p>}

        <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded">
          Login
        </button>
      </form>
    </div>
  );
}
