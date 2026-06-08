import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      'shared-types': path.resolve(__dirname, '../boss-shared-types'),
    },
  },
  server: {
    port: 3002,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/hrcomment': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
