import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { inter } from "@/app/ui/fonts";
import "./globals.css";
import MainNav from "@/app/ui/mainNav";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    template: "%s | LiveActive",
    default: "LiveActive",
  },
  description: "Example site called LiveActive",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-transparent text-white">
        <div className="fixed inset-0 overflow-hidden">
          <div className="absolute -top-[300px] -right-[300px] w-[600px] h-[600px] rounded-full bg-gradient-to-br from-green-500/20 to-emerald-700/30 blur-3xl animate-float-slow"></div>

          <div className="absolute top-[40%] -left-[200px] w-[400px] h-[400px] rounded-full bg-gradient-to-tr from-green-600/20 to-teal-500/20 blur-2xl animate-float-medium"></div>

          <div className="absolute bottom-[10%] right-[20%] w-[300px] h-[300px] rounded-full bg-gradient-to-bl from-emerald-400/20 to-green-800/30 blur-xl animate-float-fast"></div>

          <div className="absolute top-[30%] right-[10%] w-[500px] h-[200px] rounded-full bg-gradient-to-l from-green-700/20 to-teal-600/10 blur-2xl animate-pulse-slow"></div>
        </div>
        <MainNav />
        {children}
      </body>
    </html>
  );
}
