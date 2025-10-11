import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'
import { visualizer } from 'rollup-plugin-visualizer'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const isProduction = mode === 'production'
  
  return {
    plugins: [
      react({
        // Enable React Fast Refresh in development
        fastRefresh: !isProduction,
        // Optimize JSX in production
        jsxRuntime: 'automatic'
      }),
      tailwindcss(),
      // Bundle analyzer - only in production
      isProduction && visualizer({
        filename: 'dist/stats.html',
        open: false,
        gzipSize: true,
        brotliSize: true
      })
    ].filter(Boolean),
    
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
      
      // Optimize chunk splitting for better caching
      rollupOptions: {
        output: {
          // More granular chunk splitting
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
              '@radix-ui/react-accordion',
              '@radix-ui/react-alert-dialog'
            ],
            'ui-forms': [
              '@radix-ui/react-checkbox',
              '@radix-ui/react-radio-group',
              '@radix-ui/react-select',
              '@radix-ui/react-slider',
              '@radix-ui/react-switch',
              'react-hook-form',
              '@hookform/resolvers'
            ],
            'ui-feedback': [
              '@radix-ui/react-toast',
              '@radix-ui/react-tooltip',
              '@radix-ui/react-progress',
              'sonner'
            ],
            
            // Animation libraries
            'animations': ['framer-motion'],
            
            // 3D and visualization (heavy libraries)
            'three-vendor': ['three', '@react-three/fiber', '@react-three/drei'],
            
            // PDF and document generation (heavy libraries)
            'pdf-vendor': ['react-pdf', '@react-pdf/renderer', 'html2canvas'],
            
            // Utilities
            'utils': [
              'clsx',
              'tailwind-merge',
              'class-variance-authority',
              'date-fns'
            ],
            
            // Date and time
            'date-vendor': ['react-day-picker'],
            
            // Charts and data visualization
            'charts': ['recharts'],
            
            // Theme and styling
            'theme': ['next-themes']
          },
          
          // Optimize asset naming for better caching
          chunkFileNames: (chunkInfo) => {
            const facadeModuleId = chunkInfo.facadeModuleId
            if (facadeModuleId) {
              const fileName = path.basename(facadeModuleId, path.extname(facadeModuleId))
              return `js/${fileName}-[hash].js`
            }
            return 'js/[name]-[hash].js'
          },
          assetFileNames: (assetInfo) => {
            const info = assetInfo.name.split('.')
            const ext = info[info.length - 1]
            if (/\.(png|jpe?g|gif|svg|webp|ico)$/i.test(assetInfo.name)) {
              return `images/[name]-[hash].${ext}`
            }
            if (/\.(woff2?|eot|ttf|otf)$/i.test(assetInfo.name)) {
              return `fonts/[name]-[hash].${ext}`
            }
            return `assets/[name]-[hash].${ext}`
          }
        }
      },
      
      // Increase chunk size warning limit since we're optimizing chunks
      chunkSizeWarningLimit: 600,
      
      // Enable CSS code splitting
      cssCodeSplit: true,
      
      // Optimize dependencies
      commonjsOptions: {
        include: [/node_modules/],
        transformMixedEsModules: true
      }
    },
    
    // Optimize dependencies
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
        // Exclude heavy libraries from pre-bundling to allow better chunking
        'three',
        '@react-three/fiber',
        '@react-three/drei',
        'react-pdf',
        '@react-pdf/renderer'
      ]
    },
    
    server: {
      port: 5173,
      open: true,
      // Enable HMR optimizations
      hmr: {
        overlay: true
      }
    },
    
    preview: {
      port: 4173,
      open: true
    },
    
    // Enable experimental features for better performance
    esbuild: {
      // Remove console.log in production
      drop: isProduction ? ['console', 'debugger'] : [],
      // Optimize for modern browsers in production
      target: isProduction ? 'es2020' : 'es2017'
    },
    
    // CSS optimization
    css: {
      devSourcemap: !isProduction,
      postcss: {
        plugins: isProduction ? [
          // Add CSS optimization plugins for production
          require('autoprefixer'),
          require('cssnano')({
            preset: 'default'
          })
        ] : []
      }
    },
    
    // Define environment variables
    define: {
      __DEV__: !isProduction,
      __PROD__: isProduction,
      // Remove React DevTools in production
      __REACT_DEVTOOLS_GLOBAL_HOOK__: isProduction ? '({ isDisabled: true })' : undefined
    }
  }
})
