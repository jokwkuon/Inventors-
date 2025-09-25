/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // all JS/TS/JSX/TSX files in src
  ],
  theme: {
    extend: {
      colors: {
        primary: "#61dafb", // optional: add custom colors
        background: "#121212",
        card: "#1e1e1e",
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
