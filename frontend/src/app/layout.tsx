import type { Metadata } from "next";
import { Fraunces, Space_Grotesk } from "next/font/google";
import "../styles/globals.css";
import { Navigation } from "../components/Navigation";

const fontSans = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});

const fontSerif = Fraunces({
  subsets: ["latin"],
  variable: "--font-serif",
  display: "swap",
});

export const metadata: Metadata = {
  title: "AuditCare Timeline",
  description: "AI-powered patient timeline MVP",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className={`${fontSans.variable} ${fontSerif.variable}`}>
        <div className="site-shell">
          <Navigation />
          <div className="app-content">{children}</div>
        </div>
      </body>
    </html>
  );
}
