import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  base: process.env.NODE_ENV === 'production' ? '/Will-and-POA-App/' : '/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'esbuild',
    chunkSizeWarningLimit: 1000, // Increase warning limit to 1MB
    rollupOptions: {
      output: {
        // Simplified chunk splitting to reduce potential loading issues
        manualChunks: (id) => {
          // Single vendor chunk for all node_modules
          if (id.includes('node_modules')) {
            // Split out large libraries to separate chunks
            if (id.includes('@react-pdf') || id.includes('pdfjs-dist')) {
              return 'pdf-lib';
            }
            if (id.includes('three') || id.includes('@react-three')) {
              return '3d-lib';
            }
            // All other dependencies in single vendor chunk for reliability
            return 'vendor';
          }
        },
        // Ensure consistent naming for better caching
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    }
  },
  server: {
    port: 5173,
    open: true
  },
  preview: {
    port: 4173,
    open: true
  }
})
