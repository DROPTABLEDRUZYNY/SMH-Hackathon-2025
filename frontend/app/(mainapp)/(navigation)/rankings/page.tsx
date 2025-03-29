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
        const response = await fetch('http://localhost:8000/api/leaderboard', {
          credentials: 'include',
        });
        
        if (!response.ok) {
          throw new Error('Failed to fetch leaderboard data');
        }

        const data = await response.json();
        setUsers(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
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
    <div className="flex flex-col md:flex-col gap-4 md:overflow-hidden mt-32">
      {users.map((user) => (
        <UserActivity 
          key={user.id} 
          userData={{
            id: user.id,
            name: `${user.first_name} ${user.last_name}`,
            email: "", // Możemy dodać email jeśli będzie dostępny w API
            avatar_img_url: "/avatars/default.png", // Domyślny avatar
            route_img_url: "/example/route1.png", // Domyślny obraz trasy
            text: `Collected ${user.total_kg}kg of trash in ${user.total_activities} activities`,
            date: new Date().toISOString(), // Aktualna data
          }} 
        />
      ))}
    </div>
  );
}
