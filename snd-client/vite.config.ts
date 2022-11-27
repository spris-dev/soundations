import path from "path"
import { defineConfig } from "vite"
import preact from "@preact/preset-vite"

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: [
      { find: "snd-client", replacement: path.resolve(__dirname, "src") },
      {
        find: "snd-server-api-client",
        replacement: path.resolve(__dirname, "..", "snd-server-api-client"),
      },
    ],
  },
  plugins: [preact()],
  build: {
    assetsDir: "static",
  },
  envDir: path.resolve(__dirname, ".."),
  server: {
    proxy: {
      "/api": {
        target: `http://${process.env.SND_SERVER_HOST}:${process.env.SND_SERVER_PORT}`,
      },
    },
  },
})
