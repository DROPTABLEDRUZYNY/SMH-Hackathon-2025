import clsx from "clsx";
import Image from "next/image";
import { MapIcon } from "@heroicons/react/24/outline";

interface UserData {
  id: number;
  rank: number;
  name: string;
  email: string;
  avatar_img_url: string;
  route_img_url: string;
  text_trash: string;
  text_activities: string;
  date: string;
}

export default function UserActivity({ userData }: { userData: UserData }) {
  const dateObject = new Date(userData.date);
  const formattedDate = dateObject.toLocaleDateString();
  const gradientColor =
    userData.rank === 1
      ? "from-amber-400/70 via-black to-amber-400/70"
      : userData.rank === 2
      ? "from-white/70 via-black to-white/70"
      : userData.rank === 3
      ? "from-amber-800/70 via-black to-amber-800/70"
      : "from-lime-800/40 via-black to-lime-800/40";
  return (
    <div
      key={userData.id}
      className={`flex flex-col bg-gradient-to-br ${gradientColor} rounded-lg w-full`}
    >
      <div className="flex flex-row items-center justify-between  bg-transparent px-7 py-4 w-full">
        <div className="flex items-center bg-transparent w-[50%]">
          <Image
            src="/avatars/avatar1.png"
            alt={`${userData.name}'s profile picture`}
            className="mr-4 rounded-full"
            width={40}
            height={40}
          />
          <div className="min-w-0 mr-2 bg-transparent">
            <p className="truncate text-sm font-semibold md:text-base bg-transparent">
              {userData.name}
            </p>
            <p className="hidden text-sm text-gray-500 sm:block bg-transparent">
              {userData.email}
            </p>
          </div>
        </div>
        <div className="flex justify-start gap-34 mx-5 bg-transparent">
          <p className="bg-transparent font-bold">{userData.text_trash}</p>
          <p className="bg-transparent">{userData.text_activities}</p>
        </div>
        <div
          className={`truncate text-sm font-medium md:text-base bg-transparent`}
        >
          <p>{formattedDate}</p>
        </div>
      </div>
    </div>
  );
}
