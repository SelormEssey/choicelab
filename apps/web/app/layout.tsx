import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ChoiceLab | Human-AI decision research",
  description:
    "Exploring how recommendations, explanations, and confidence cues affect human decision-making and reliance.",
  icons: {
    icon: "/favicon.svg",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" data-scroll-behavior="smooth">
      <body>{children}</body>
    </html>
  );
}
