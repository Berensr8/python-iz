import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Python İz · Kodu anla, kendin yaz",
  description: "Türkçe, interaktif Python öğrenme alanı. Kodu oku, hataları düzelt, kendi programlarını yaz ve test et.",
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
