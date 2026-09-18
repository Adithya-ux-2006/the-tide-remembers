import type { Metadata } from "next";
import { Caveat, Cormorant_Garamond, Inter } from "next/font/google";
import "./globals.css";

const caveat = Caveat({
  variable: "--font-caveat",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

const cormorant = Cormorant_Garamond({
  variable: "--font-cormorant",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600"],
  style: ["normal", "italic"],
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600"],
});

export const metadata: Metadata = {
  title: "Our Story — A Digital Diary",
  description: "A private digital diary celebrating three beautiful years together.",
  robots: {
    index: false,
    follow: false,
  },
};

export default function RootLayout({
  children,
}: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${caveat.variable} ${cormorant.variable} ${inter.variable} antialiased`}
    >
      <body className="min-h-screen bg-paper text-ink">
        {children}
      </body>
    </html>
  );
}
