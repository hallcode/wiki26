import { defineConfig } from 'vite'
import path from 'path'

export default defineConfig({
  server: {
    port: 5173,
    strictPort: true,
    origin: 'http://localhost:5173'
  },
  build: {
    outDir: 'static/dist',
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: path.resolve(__dirname, 'wiki/core/assets/js/main.js')
    }
  }
})
