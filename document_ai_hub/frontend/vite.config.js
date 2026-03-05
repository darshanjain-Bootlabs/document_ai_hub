import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path';
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: 'localhost',
    port: 5173,
    hmr: {
      host: 'localhost',
      port: 5173,
    },
  },

  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
