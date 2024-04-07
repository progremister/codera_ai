"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Montserrat } from "next/font/google";

import { cn } from "@/lib/utils";
import {
  User2Icon,
  Cog
  } from "lucide-react";

  import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
  } from "@/components/ui/accordion"

  import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
  } from "@/components/ui/dropdown-menu"

const montserrat = Montserrat({ weight: "600", subsets: ["latin"] });

const routes = [
  {
    label: "Administration",
    icon: User2Icon,
    href: "https://www.mendable.ai/app/6792/conversations",
    color: "text-sky-500",
  },
];

const Sidebar = () => {
  const pathname = usePathname();
  return (
    <div className="space-y-4 py-4 flex flex-col h-full bg-[#111827] text-white">
      <div className="px-3 py-2 flex-1">
        <Link href="/" className="flex items-center pl-3 mb-1 gap-3 align-center justify-start">
        <img
            src="images/codera_image.png"
            className="h-12 w-12 rounded-full bg-white"
            alt="assistant"
          />
          <h1
            className={cn(
              "text-3xl text-transparent font-extralight bg-clip-text bg-gradient-to-r from-violet-800 to-[#ea0a8e]",
              montserrat.className
            )}
          >
            Codera
          </h1>
        </Link>
        <div className="space-y-1 m-auto mt-10">
          {routes.map((route) => (
            <Link
              href={route.href}
              key={route.href}
              className={cn(
                "text-sm group flex p-3 w-full justify-center font-medium cursor-pointer hover:text-white hover:bg-white/10 rounded-lg transition",
                pathname === route.href
                  ? "text-white bg-white/10"
                  : "text-zinc-400"
              )}
            >
              <div className="flex items-center flex-1">
                <route.icon className={cn("h-5 w-5 mr-3", route.color)} />
                {route.label}
              </div>
            </Link>
          ))}
                          
          <div className="flex items-center flex-1">          
          <Accordion type="single" collapsible className="flex gap-1 items-center align-center text-sm p-3 w-fullfont-medium cursor-pointer hover:text-white hover:bg-white/10 rounded-lg transition">
            <Cog className="h-5 w-5 mr-3" />         
            <AccordionItem value="item-1">
              <AccordionTrigger>Personalisation</AccordionTrigger>
              <AccordionContent className="flex flex-col gap-2 justify-start items-start">
              <DropdownMenu>
                <DropdownMenuTrigger>Select Role</DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuLabel>Role</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem>Developer</DropdownMenuItem>
                  <DropdownMenuItem>UX/UI Designer</DropdownMenuItem>
                  <DropdownMenuItem>DevOps</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>

              <DropdownMenu>
                <DropdownMenuTrigger>Select Experience</DropdownMenuTrigger>
                  <DropdownMenuContent>
                    <DropdownMenuLabel>Experience</DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem>Newbie</DropdownMenuItem>
                    <DropdownMenuItem>Experienced</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
          </div>

        </div>
      </div>
    </div>
  );
};

export default Sidebar;
