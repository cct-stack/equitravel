/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        racing: {
          green: "#1a472a",
          gold: "#c9a84c",
          cream: "#f5f0e8",
          dark: "#0d1117",
          slate: "#1e293b",
        },
      },
      fontFamily: {
        serif: ["Georgia", "Cambria", "Times New Roman", "serif"],
      },
    },
  },
  plugins: [],
};
