"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";

type RegisterForm = {
  email: string;
  password: string;
  confirmPassword: string;
};

export default function RegisterPage() {
  const [error, setError] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<RegisterForm>();

  const onSubmit = async (data: RegisterForm) => {
    if (data.password !== data.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/api/users/auth/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: data.email, password: data.password }),
      });

      if (!res.ok) throw new Error("Registration failed");
      console.log("Registered successfully!");
    } catch (err) {
      setError("Registration failed");
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-4">Register</h1>
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
          {...register("password", { required: "Password is required", minLength: 6 })}
          type="password"
          placeholder="Password"
          className="w-full p-2 border border-gray-300 rounded"
        />
        {errors.password && <p className="text-red-500">{errors.password.message}</p>}

        <input
          {...register("confirmPassword", { required: "Please confirm password" })}
          type="password"
          placeholder="Confirm Password"
          className="w-full p-2 border border-gray-300 rounded"
        />
        {errors.confirmPassword && <p className="text-red-500">{errors.confirmPassword.message}</p>}

        <button type="submit" className="w-full bg-green-600 text-white p-2 rounded">
          Register
        </button>
      </form>
    </div>
  );
}
