import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Load env file based on `mode` in the current working directory.
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [react()],
    base: '/', // Ensure base URL is set correctly
    build: {
      outDir: 'dist',
      sourcemap: true,
      rollupOptions: {
        output: {
          manualChunks: undefined
        }
      }
    },
    server: {
      port: 5173,
      host: '0.0.0.0'
    },
    define: {
      'process.env.VITE_API_URL': JSON.stringify(env.VITE_API_URL || 'https://sambhar-production.up.railway.app')
    }
  }
})
