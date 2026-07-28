import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Norynthe Investor Access | Independent AI Trust Infrastructure",
  description: "Controlled investor diligence for Norynthe’s research discipline, working evaluation OS, capital plan, and independent AI trust thesis.",
  icons: {
    icon: "/favicon.png",
    shortcut: "/favicon.png",
    apple: "/favicon.png",
  },
  openGraph: {
    title: "Norynthe Investor Access",
    description: "From research discipline to independent AI trust infrastructure.",
    type: "website",
    images: [{ url: "/og.png", width: 1200, height: 630, alt: "Norynthe — Independent infrastructure for AI trust" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Norynthe Investor Access",
    description: "From research discipline to independent AI trust infrastructure.",
    images: ["/og.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
