import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        orbitron: ["Orbitron", "sans-serif"],
        sans: ["Inter", "sans-serif"],
      },
      colors: {
        // Dark theme inspired by f1-dash.com
        background: "#09090b",
        foreground: "#fafafa",
        primary: {
          DEFAULT: "#e10600", // F1 Red
          foreground: "#fafafa",
        },
        secondary: {
          DEFAULT: "#18181b",
          foreground: "#fafafa",
        },
        muted: {
          DEFAULT: "#27272a",
          foreground: "#a1a1aa",
        },
        accent: {
          DEFAULT: "#3f3f46",
          foreground: "#fafafa",
        },
        card: {
          DEFAULT: "#18181b",
          foreground: "#fafafa",
        },
        border: "#27272a",
      },
      borderRadius: {
        lg: "0.75rem",
        md: "0.5rem",
        sm: "0.25rem",
      },
    },
  },
  plugins: [],
};

export default config;
