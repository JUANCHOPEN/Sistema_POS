import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  preview: {
    host: "0.0.0.0",
    allowedHosts: [
      "sistema-pos-5qbk.onrender.com"
    ]
  },
  server: {
    host: "0.0.0.0"
  }
});
