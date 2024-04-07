import Sidebar from "@/components/sidebar";
import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Navbar from "@/components/navbar";
import Head from "next/head";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "CODERA Chatbot",
  description: "Chatbot with custom knowledge base",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <Head>
        <link rel="icon" href="/favicons/favicon.ico" />
        <link
          rel="icon"
          href="favicons/favicon-32x32.png"
          type="image/png"
          sizes="32x32"
        />
        <link
          rel="icon"
          href="/favicons/favicon-16x16.png"
          type="image/png"
          sizes="16x16"
        />
      </Head>
      <div className="h-full relative">
        <div className="hidden h-full md:flex md:w-72 md:flex-col md:fixed md:inset-y-0 z-80 bg-gray-900">
          <Sidebar />
        </div>
        <main className="md:pl-72 ">
          <Navbar />
          {children}
        </main>
      </div>
    </>
  );
}
