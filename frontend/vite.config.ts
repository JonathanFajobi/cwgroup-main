import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  base:
    mode === "development"
      ? "http://127.0.0.1/"
      : "/static/api/spa/",
  build: {
    emptyOutDir: true,
    outDir: "../api/static/api/spa",
  },
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: '127.0.0.1',   // Set the host to 127.0.0.1
    port: 5173,           // Ensure the port is 5173 or any port you prefer
  }
}));
