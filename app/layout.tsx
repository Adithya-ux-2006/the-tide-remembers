import type { Metadata } from "next";
import { Bebas_Neue, Inter } from "next/font/google";
import "./globals.css";

const bebas = Bebas_Neue({
  variable: "--font-bebas",
  subsets: ["latin"],
  weight: "400",
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: "US+",
  description: "Our story, streaming.",
  robots: { index: false, follow: false },
};

export default function RootLayout({
  children,
}: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${bebas.variable} ${inter.variable} antialiased`}>
      <body className="min-h-screen bg-bg text-text overflow-x-hidden">
        {children}
      </body>
    </html>
  );
}
