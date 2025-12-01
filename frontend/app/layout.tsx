import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ApexData - F1 Telemetry & Analytics",
  description: "Formula 1 telemetry data and analytics platform powered by FastF1",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.Node;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
