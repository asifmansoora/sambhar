import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          'mantine': ['@mantine/core', '@mantine/hooks', '@mantine/dropzone'],
          'plotly': ['plotly.js-dist-min', 'react-plotly.js'],
        },
      },
    },
  },
  server: {
    port: 5173,
    host: true,
  },
})
