"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

interface NavItem {
  name: string;
  href: string;
  icon: string;
  section?: "live" | "general";
}

const navItems: NavItem[] = [
  // Live Timing Section
  { name: "Dashboard", href: "/dashboard", icon: "📊", section: "live" },
  { name: "Track Map", href: "/track-map", icon: "🗺️", section: "live" },
  { name: "Standings", href: "/standings", icon: "🏆", section: "live" },
  { name: "Weather", href: "/weather", icon: "🌤️", section: "live" },

  // General Section
  { name: "Seasons", href: "/seasons", icon: "📅", section: "general" },
  { name: "Drivers", href: "/drivers", icon: "🏎️", section: "general" },
  { name: "Constructors", href: "/constructors", icon: "🏁", section: "general" },
  { name: "Races", href: "/races", icon: "🏁", section: "general" },
  { name: "Telemetry", href: "/telemetry", icon: "📈", section: "general" },
  { name: "Settings", href: "/settings", icon: "⚙️", section: "general" },
];

export default function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const pathname = usePathname();

  const liveItems = navItems.filter(item => item.section === "live");
  const generalItems = navItems.filter(item => item.section === "general");

  return (
    <aside
      className={`fixed left-0 top-0 h-screen bg-card border-r border-border transition-all duration-300 z-50 ${
        isCollapsed ? "w-16" : "w-64"
      }`}
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border">
        {!isCollapsed && (
          <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-red-600 bg-clip-text text-transparent">
            ApexData
          </h1>
        )}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="p-2 rounded-lg hover:bg-accent transition-colors"
          aria-label="Toggle sidebar"
        >
          {isCollapsed ? "→" : "←"}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col p-4 space-y-6">
        {/* Live Timing Section */}
        <div>
          {!isCollapsed && (
            <h2 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">
              Live Timing
            </h2>
          )}
          <ul className="space-y-1">
            {liveItems.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                    pathname === item.href
                      ? "bg-primary text-primary-foreground"
                      : "hover:bg-accent text-muted-foreground hover:text-foreground"
                  }`}
                  title={isCollapsed ? item.name : undefined}
                >
                  <span className="text-xl">{item.icon}</span>
                  {!isCollapsed && (
                    <span className="font-medium">{item.name}</span>
                  )}
                </Link>
              </li>
            ))}
          </ul>
        </div>

        {/* General Section */}
        <div>
          {!isCollapsed && (
            <h2 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">
              General
            </h2>
          )}
          <ul className="space-y-1">
            {generalItems.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                    pathname === item.href
                      ? "bg-primary text-primary-foreground"
                      : "hover:bg-accent text-muted-foreground hover:text-foreground"
                  }`}
                  title={isCollapsed ? item.name : undefined}
                >
                  <span className="text-xl">{item.icon}</span>
                  {!isCollapsed && (
                    <span className="font-medium">{item.name}</span>
                  )}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </nav>

      {/* Footer */}
      {!isCollapsed && (
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-border">
          <div className="flex items-center gap-3">
            <a
              href="https://github.com/mickstmt/ApexData.py"
              target="_blank"
              rel="noopener noreferrer"
              className="text-muted-foreground hover:text-foreground transition-colors"
              title="GitHub"
            >
              GitHub
            </a>
            <span className="text-muted-foreground">•</span>
            <span className="text-xs text-muted-foreground">v1.0.0</span>
          </div>
        </div>
      )}
    </aside>
  );
}
