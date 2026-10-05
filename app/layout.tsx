import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Python İz · Kodu okuyarak Python öğren",
  description: "Türkçe, interaktif ve kod okuma odaklı Python öğrenme alanı.",
  other: {
    "codex-preview": "development",
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="tr" className="dark" suppressHydrationWarning>
      <body className="antialiased">{children}</body>
    </html>
  );
}
