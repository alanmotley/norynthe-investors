import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://investors.norynthe.com"),
  title: "Norynthe Investor Access | Independent AI Evaluation Laboratory",
  description: "Selected diligence on Norynthe’s independent AI evaluation laboratory, founder-built foundation, capital-to-capability plan, and proof program.",
  robots: {
    index: false,
    follow: false,
    noarchive: true,
    noimageindex: true,
    nocache: true,
  },
  icons: {
    icon: "/favicon.png",
    shortcut: "/favicon.png",
    apple: "/favicon.png",
  },
  openGraph: {
    title: "Norynthe Investor Access",
    description: "Building the independent laboratory for AI trust.",
    type: "website",
    images: [{ url: "/og.png", width: 1200, height: 630, alt: "Norynthe — Independent infrastructure for AI trust" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Norynthe Investor Access",
    description: "Building the independent laboratory for AI trust.",
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
