"use client";

import Image from "next/image";
import UserActivity from "@/app/ui/activity/userActivity";
import { useEffect, useState } from "react";

interface LeaderboardUser {
  id: number;
  first_name: string;
  last_name: string;
  total_kg: number;
  total_activities: number;
}

export default function Page() {
  const [users, setUsers] = useState<LeaderboardUser[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/leaderboard", {
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Failed to fetch leaderboard data");
        }

        const data = await response.json();
        setUsers(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setIsLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-xl text-red-500">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4 md:overflow-hidden mt-32 bg-transparent justify-center items-center">
      <h1 className="text-3xl font-bold text-white mb-6 glow">Rankings</h1>

      {/* Заголовки колонок */}
      <div className="flex flex-row w-full items-center justify-between px-7 py-3 mb-4 border-b border-white/20">
        <div className=" w-[50%]">
          <h2 className="text-sm font-semibold text-white/80 uppercase tracking-wider">
            Name
          </h2>
        </div>
        <div className="flex gap-10 mx-10">
          <h2 className="text-sm font-semibold text-white/80 uppercase tracking-wider">
            Trash collected
          </h2>
          <h2 className="text-sm font-semibold text-white/80 uppercase tracking-wider">
            Activity
          </h2>
        </div>
        <div>
          <h2 className="text-sm font-semibold text-white/80 uppercase tracking-wider">
            Date
          </h2>
        </div>
      </div>
      {users.map((user, index) => (
        <UserActivity
          key={user.id}
          userData={{
            id: user.id,
            rank: index + 1,
            name: `${user.first_name} ${user.last_name}`,
            email: "", // Możemy dodać email jeśli będzie dostępny w API
            avatar_img_url: "/avatars/default.png", // Domyślny avatar
            route_img_url: "/example/route1.png", // Domyślny obraz trasy
            text_trash: `${user.total_kg}kg`,
            text_activities: `${user.total_activities}`,
            date: new Date().toISOString(), // Aktualna data
          }}
        />
      ))}
    </div>
  );
}
