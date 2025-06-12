import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/recommend': 'http://localhost:8000',
      '/events': 'http://localhost:8000',
      '/speakers': 'http://localhost:8000'
    }
  }
})
