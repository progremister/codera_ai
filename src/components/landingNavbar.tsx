"use client";

import { Montserrat } from "next/font/google";
import Image from "next/image";
import Link from "next/link";
import { useAuth } from "@clerk/nextjs";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

const font = Montserrat({
  weight: "600",
  subsets: ["latin"],
});

const LandingNavbar = () => {
  const { isSignedIn } = useAuth();

  return (
    <nav className="p-4 bg-transparent flex items-center justify-between">
      <Link href="/" className="">
        <div className="flex row items-center gap-3 text-3xl text-transparent font-semibold bg-clip-text bg-gradient-to-r from-violet-800 to-[#ea0a8e]">
        <img
            src="images/codera_image.png"
            className="h-14 w-14 rounded-full bg-white"
            alt="assistant"
          />        
          Codera
        </div>
      </Link>
      <div className="flex items-center gap-x-2">
        <Link href={isSignedIn ? "/chat" : "/sign-in"}>
          <Button className="rounded-full bg-gradient-to-r from-violet-800 to-[#ea0a8e]">
            Get Started
          </Button>
        </Link>
      </div>
    </nav>
  );
};

export default LandingNavbar;
