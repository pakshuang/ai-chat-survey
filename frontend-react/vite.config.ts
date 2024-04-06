import { defineConfig } from "vite";
import dotenv from 'dotenv';
import react from "@vitejs/plugin-react";
dotenv.config();
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    strictPort: true,
    port: Number(process.env.FRONTEND_CONTAINER_PORT || 5173),
  },
});
