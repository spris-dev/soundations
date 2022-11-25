import path from "path"
import { defineConfig } from "vite"
import preact from "@preact/preset-vite"

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: [
      { find: "snd-client", replacement: path.resolve(__dirname, "src") },
    ],
  },
  plugins: [preact()],
  build: {
    assetsDir: "static",
  },
})
