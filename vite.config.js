import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: process.env.NODE_ENV === 'production'
    ? '/2025-Taipei-City-Dashboard-Teamwork/'
    : '/',
  build: {
    outDir: 'dist'
  },
  server: {
    port: 3000
  }
})
