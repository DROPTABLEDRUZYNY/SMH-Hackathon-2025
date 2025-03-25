"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { login } from "@/services/authService";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

type LoginForm = {
  email: string;
  password: string;
};

export default function LoginPage() {
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>();
  const router = useRouter();

  const onSubmit = async (data: LoginForm) => {
    try {
      const sessionId = await login(data.email, data.password);
      setSessionId(sessionId || null);
      console.log("Logged in!");
      router.push("/");
    } catch (err) {
      setError("Invalid email or password");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-4">Login</h1>
      {error && <p className="text-red-500">{error}</p>}
      {sessionId && <p className="text-green-500">Session ID: {sessionId}</p>}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <Input
          {...register("email", { required: "Email is required" })}
          type="email"
          placeholder="Email"
          className="w-full p-2 border border-gray-300 rounded"
        />
        {errors.email && <p className="text-red-500">{errors.email.message}</p>}

        <Input
          {...register("password", { required: "Password is required" })}
          type="password"
          placeholder="Password"
          className="w-full p-2 border border-gray-300 rounded"
        />
        {errors.password && (
          <p className="text-red-500">{errors.password.message}</p>
        )}

        <Button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white p-2 rounded"
        >
          Login
        </Button>
      </form>
    </div>
  );
}
