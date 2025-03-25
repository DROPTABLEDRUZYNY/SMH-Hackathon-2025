import type { Metadata } from "next";
import "@/app/globals.css";
import { inter } from "@/app/ui/fonts";

import localFont from "next/font/local";
import MainNav from "@/app/ui/mainNav";

export const metadata: Metadata = {
  title: {
    template: "%s | LiveActive",
    default: "LiveActive",
  },
  description: "Example site called LiveActive",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <span lang="en" suppressHydrationWarning>
      <div className="flex h-screen flex-col md:flex-row md:overflow-hidden">
        <div className="w-full flex-none md:w-64">
          <MainNav />
        </div>
        <div className="flex-grow p-6 md:overflow-y-auto md:p-10">
          {children}
        </div>
      </div>
    </span>
  );
}
