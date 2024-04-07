"use client";

import { useAuth } from "@clerk/nextjs";
import Link from "next/link";
import TypewriterComponent from "typewriter-effect";
import { Button } from "@/components/ui/button";

const LandingHero = () => {
  const { isSignedIn } = useAuth();
  return (
    <div className="text-white font-bold py-36 text-center space-y-5">
      <div className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl space-y-5 font-extrabold">
        <h1>The revolutionary AI Tool for</h1>
        <div className="text-transparent bg-clip-text bg-gradient-to-r from-violet-800 to-[#ea0a8e]">
          <TypewriterComponent
            options={{
              strings: [
                "Code Update.",
                "Code Refactoring.",
                "Efectivity.",
                "Problem-Solving.",
              ],
              autoStart: true,
              loop: true,
            }}
          />
        </div>
      </div>
      <div className="text-lg md:text-xl font-light text-zinc-400">
            Update the legacy 10x faster.
      </div>
      <div>
        <Link href={isSignedIn ? "/chat" : "/sign-in"}>
            <Button  className="md:text-lg p-4 md:p-6 rounded-full font-semibold bg-gradient-to-r from-violet-800 to-[#ea0a8e]">
                Talk to Codera
            </Button>
        </Link>
      </div>
    </div>
  );
};

export default LandingHero;
