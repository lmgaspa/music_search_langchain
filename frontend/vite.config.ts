import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'https://music-search-langchain.onrender.com',
        changeOrigin: true,
        // strip the /api prefix -> backend sees /xxx
        rewrite: (path) => path.replace(/^\/api/, ''),
        ws: true,
        xfwd: true,
        timeout: 60_000,
        proxyTimeout: 60_000,
        secure: true, // Render uses valid certs; set false only for self-signed
        configure: (proxy) => {
          proxy.on('error', (err) => {
            console.log('proxy error', err)
          })
          proxy.on('proxyReq', (_, req) => {
            console.log('Sending Request to the Target:', req.method, req.url)
          })
          proxy.on('proxyRes', (proxyRes, req) => {
            console.log('Received Response from the Target:', proxyRes.statusCode, req.url)
          })
        },
      },
    },
  },
})
