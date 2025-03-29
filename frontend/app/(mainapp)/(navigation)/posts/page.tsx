"use client";

import { useEffect, useState } from "react";
import Image from "next/image";

interface TrashPlace {
  id: number;
  name: string;
  description: string;
  date_created: string;
  latitude: number;
  longitude: number;
  is_active: boolean;
}

interface Post {
  id: number;
  description: string;
  date: string;
  trash_place: TrashPlace;
  collected_kg: number;
  cleaned_all: boolean;
  before_image: string | null;
  after_image: string | null;
}

export default function PostsPage() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/activities", {
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Failed to fetch posts");
        }

        const data = await response.json();
        // Sortuj posty od najnowszych
        const sortedPosts = data.sort((a: Post, b: Post) => 
          new Date(b.date).getTime() - new Date(a.date).getTime()
        );
        setPosts(sortedPosts);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setIsLoading(false);
      }
    };

    fetchPosts();
  }, []);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-xl text-white animate-pulse">Loading...</div>
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
    <div className="container mx-auto px-4 py-8 mt-20 max-w-5xl">
      <h1 className="text-4xl font-bold text-white mb-8 text-center tracking-tight">
        Activity Feed
      </h1>
      <div className="space-y-8">
        {posts.map((post) => (
          <div 
            key={post.id} 
            className="bg-white/5 backdrop-blur-lg rounded-xl p-6 space-y-6 border border-white/10 hover:border-white/20 transition-all duration-300 shadow-lg hover:shadow-xl"
          >
            <div className="flex bg-transparent justify-between items-start gap-4">
              <div className="bg-transparent flex-1">
                <h2 className="bg-transparent text-2xl font-semibold text-white mb-3 tracking-tight">
                  {post.trash_place.name}
                </h2>
                <p className="text-gray-300 leading-relaxed">
                  {post.description}
                </p>
              </div>
              <div className="bg-transparent text-right flex flex-col items-end">
                <div className="bg-green-500/10 px-4 py-2 rounded-full mb-2">
                  <p className="text-green-400 font-bold text-lg">
                    {post.collected_kg} kg
                  </p>
                </div>
                <p className="text-gray-400 text-sm">
                  {new Date(post.date).toLocaleDateString('pl-PL', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </p>
              </div>
            </div>

            {(post.before_image || post.after_image) && (
              <div className="bg-transparent grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
                {post.before_image && (
                  <div className="bg-transparent space-y-2">
                    <p className="text-gray-400 font-medium">Before</p>
                    <div className="bg-transparent relative h-[250px] w-full overflow-hidden rounded-lg">
                      <Image
                        src={post.before_image}
                        alt="Before cleaning"
                        fill
                        className="object-cover hover:scale-105 transition-transform duration-300"
                      />
                    </div>
                  </div>
                )}
                {post.after_image && (
                  <div className="space-y-2 bg-transparent">
                    <p className="text-gray-400 font-medium">After</p>
                    <div className="relative bg-transparent h-[250px] w-full overflow-hidden rounded-lg">
                      <Image
                        src={post.after_image}
                        alt="After cleaning"
                        fill
                        className="object-cover hover:scale-105 transition-transform duration-300"
                      />
                    </div>
                  </div>
                )}
              </div>
            )}

            <div className="flex flex-wrap bg-transparent justify-between items-center pt-4 border-t border-white/5">
              <div className="flex items-center  bg-transparent space-x-2">
                <span className="text-gray-400 text-sm">
                  📍 {post.trash_place.latitude.toFixed(6)}, {post.trash_place.longitude.toFixed(6)}
                </span>
              </div>
              {post.cleaned_all && (
                <span className="bg-green-500/20 text-green-400 px-4 py-1.5 rounded-full text-sm font-medium flex items-center">
                  ✨ Fully cleaned
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
