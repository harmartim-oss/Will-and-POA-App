import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const isProduction = mode === 'production'
  
  return {
    plugins: [
      react({
        fastRefresh: !isProduction,
        jsxRuntime: 'automatic'
      }),
      tailwindcss()
    ],
    
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
      target: 'es2020',
      
      rollupOptions: {
        output: {
          manualChunks: {
            // Core React libraries
            'react-vendor': ['react', 'react-dom'],
            
            // Routing
            'router': ['react-router-dom'],
            
            // UI Framework - split by usage patterns
            'ui-core': [
              '@radix-ui/react-dialog',
              '@radix-ui/react-dropdown-menu',
              '@radix-ui/react-tabs',
              '@radix-ui/react-accordion'
            ],
            'ui-forms': [
              '@radix-ui/react-checkbox',
              '@radix-ui/react-select',
              'react-hook-form'
            ],
            
            // Animation libraries
            'animations': ['framer-motion'],
            
            // 3D libraries (lazy load these)
            'three-vendor': ['three', '@react-three/fiber', '@react-three/drei'],
            
            // PDF libraries (lazy load these)
            'pdf-vendor': ['react-pdf', '@react-pdf/renderer'],
            
            // Utilities
            'utils': ['clsx', 'tailwind-merge', 'date-fns']
          },
          
          chunkFileNames: 'js/[name]-[hash].js',
          assetFileNames: (assetInfo) => {
            const info = assetInfo.name.split('.')
            const ext = info[info.length - 1]
            if (/\.(png|jpe?g|gif|svg|webp|ico)$/i.test(assetInfo.name)) {
              return `images/[name]-[hash].${ext}`
            }
            return `assets/[name]-[hash].${ext}`
          }
        }
      },
      
      chunkSizeWarningLimit: 600,
      cssCodeSplit: true
    },
    
    optimizeDeps: {
      include: [
        'react',
        'react-dom',
        'react-router-dom',
        'framer-motion',
        'clsx',
        'tailwind-merge'
      ],
      exclude: [
        'three',
        '@react-three/fiber',
        '@react-three/drei',
        'react-pdf',
        '@react-pdf/renderer'
      ]
    },
    
    server: {
      port: 5173,
      open: true
    },
    
    preview: {
      port: 4173,
      open: true
    },
    
    esbuild: {
      drop: isProduction ? ['console', 'debugger'] : [],
      target: isProduction ? 'es2020' : 'es2017'
    }
  }
})
