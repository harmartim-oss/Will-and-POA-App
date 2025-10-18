import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'
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
      tailwindcss(),
      VitePWA({
        registerType: 'prompt',
        includeAssets: ['favicon.svg', 'robots.txt'],
        manifest: {
          name: 'Ontario Wills & Power of Attorney Creator',
          short_name: 'Ontario Wills',
          description: 'Create legally compliant wills and power of attorney documents for Ontario. AI-powered platform with professional formatting and legal expertise.',
          theme_color: '#667eea',
          background_color: '#ffffff',
          display: 'standalone',
          scope: '/Will-and-POA-App/',
          start_url: '/Will-and-POA-App/',
          orientation: 'portrait-primary',
          icons: [
            {
              src: '/Will-and-POA-App/pwa-64x64.png',
              sizes: '64x64',
              type: 'image/png'
            },
            {
              src: '/Will-and-POA-App/pwa-192x192.png',
              sizes: '192x192',
              type: 'image/png'
            },
            {
              src: '/Will-and-POA-App/pwa-512x512.png',
              sizes: '512x512',
              type: 'image/png',
              purpose: 'any'
            },
            {
              src: '/Will-and-POA-App/maskable-icon-512x512.png',
              sizes: '512x512',
              type: 'image/png',
              purpose: 'maskable'
            }
          ],
          categories: ['productivity', 'business', 'legal'],
          screenshots: [
            {
              src: '/Will-and-POA-App/screenshot1.png',
              sizes: '1280x720',
              type: 'image/png',
              label: 'Main application interface'
            }
          ]
        },
        workbox: {
          globPatterns: ['**/*.{js,css,html,ico,png,svg,woff,woff2}'],
          runtimeCaching: [
            {
              urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
              handler: 'CacheFirst',
              options: {
                cacheName: 'google-fonts-cache',
                expiration: {
                  maxEntries: 10,
                  maxAgeSeconds: 60 * 60 * 24 * 365 // 1 year
                },
                cacheableResponse: {
                  statuses: [0, 200]
                }
              }
            },
            {
              urlPattern: /^https:\/\/fonts\.gstatic\.com\/.*/i,
              handler: 'CacheFirst',
              options: {
                cacheName: 'gstatic-fonts-cache',
                expiration: {
                  maxEntries: 10,
                  maxAgeSeconds: 60 * 60 * 24 * 365 // 1 year
                },
                cacheableResponse: {
                  statuses: [0, 200]
                }
              }
            },
            {
              urlPattern: /\.(?:png|jpg|jpeg|svg|gif)$/,
              handler: 'CacheFirst',
              options: {
                cacheName: 'images-cache',
                expiration: {
                  maxEntries: 50,
                  maxAgeSeconds: 60 * 60 * 24 * 30 // 30 days
                }
              }
            },
            {
              urlPattern: /\/api\/.*/i,
              handler: 'NetworkFirst',
              options: {
                cacheName: 'api-cache',
                networkTimeoutSeconds: 10,
                expiration: {
                  maxEntries: 50,
                  maxAgeSeconds: 60 * 5 // 5 minutes
                },
                cacheableResponse: {
                  statuses: [0, 200]
                }
              }
            }
          ],
          cleanupOutdatedCaches: true,
          skipWaiting: true,
          clientsClaim: true
        },
        devOptions: {
          enabled: false,
          type: 'module'
        }
      })
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
