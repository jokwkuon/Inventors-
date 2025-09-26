import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { SiteHeader } from "@/components/site-header";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Inventors Dashboard",
  description: "Innovation radar for inventors",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased flex h-screen bg-background text-foreground`}>
        <SidebarProvider>
          {/* Sidebar */}
          <AppSidebar variant="inset" />

          {/* Main content */}
          <div className="flex-1 flex flex-col overflow-auto">
            <SiteHeader />
            <main className="p-6">{children}</main>
          </div>
        </SidebarProvider>
      </body>
    </html>
  );
}
