import React, { Suspense, lazy, useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom'
import { Toaster } from './components/ui/toaster'
import { ThemeProvider } from './components/ThemeContext'
import ErrorBoundary from './components/ui/error-boundary'
import EnhancedLoading from './components/ui/enhanced-loading'
import MobileNav from './components/ui/mobile-nav'
import { usePreload } from './components/LazyDocumentCreator'
import { config } from './config/environment'

// Lazy load components for better performance
const ModernLandingPage = lazy(() => import('./components/ModernLandingPage'))
const LazyDocumentCreator = lazy(() => import('./components/LazyDocumentCreator'))
const DocumentEditor = lazy(() => import('./components/DocumentEditor'))
const DocumentPreview = lazy(() => import('./components/DocumentPreview'))
const DemoShowcase = lazy(() => import('./components/DemoShowcase'))

// Loading component with route-specific messaging
const RouteLoading = ({ route }) => {
  const getLoadingProps = () => {
    switch (route) {
      case '/':
        return {
          message: "Loading Demo Showcase",
          submessage: "Preparing the enhanced legal document platform...",
          type: 'ai'
        }
      case '/landing':
        return {
          message: "Loading Landing Page",
          submessage: "Setting up the welcome experience...",
          type: 'default'
        }
      case '/create':
        return {
          message: "Loading Document Creator",
          submessage: "Initializing legal document wizard...",
          type: 'legal'
        }
      default:
        return {
          message: "Loading...",
          submessage: "Please wait while we prepare your content",
          type: 'default'
        }
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-blue-900">
      <EnhancedLoading {...getLoadingProps()} size="large" />
    </div>
  )
}

// Enhanced App Content with navigation and preloading
function AppContent() {
  const navigate = useNavigate()
  const location = useLocation()
  const { preload } = usePreload()
  const [mobileNavOpen, setMobileNavOpen] = useState(false)

  // Preload components on route hover/focus
  useEffect(() => {
    const preloadOnHover = (selector, componentType) => {
      const elements = document.querySelectorAll(selector)
      elements.forEach(element => {
        const handleMouseEnter = () => preload(componentType)
        element.addEventListener('mouseenter', handleMouseEnter, { once: true })
        element.addEventListener('focus', handleMouseEnter, { once: true })
      })
    }

    // Preload document creator when user hovers over CTA buttons
    preloadOnHover('[data-preload="document-creator"]', 'document-creator')
    preloadOnHover('[data-preload="premium-creator"]', 'premium-creator')
  }, [preload])

  const handleGetStarted = () => {
    navigate('/create/will')
  }

  const handleLearnMore = () => {
    const featuresSection = document.getElementById('features')
    if (featuresSection) {
      featuresSection.scrollIntoView({ behavior: 'smooth' })
    }
  }

  const handleMobileNavigation = (path) => {
    navigate(path)
    setMobileNavOpen(false)
  }

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-blue-900">
        {/* Skip link for accessibility */}
        <a href="#main" className="skip-link">Skip to main content</a>
        
        {/* Mobile Navigation */}
        <MobileNav
          isOpen={mobileNavOpen}
          onToggle={() => setMobileNavOpen(!mobileNavOpen)}
          onNavigate={handleMobileNavigation}
          currentPath={location.pathname}
          className="fixed top-4 right-4 z-50"
        />

        <main id="main" role="main" className="block focus:outline-none">
          <Routes>
            <Route 
              path="/" 
              element={
                <Suspense fallback={<RouteLoading route="/" />}>
                  <DemoShowcase />
                </Suspense>
              } 
            />
            <Route 
              path="/landing" 
              element={
                <Suspense fallback={<RouteLoading route="/landing" />}>
                  <ModernLandingPage 
                    onGetStarted={handleGetStarted} 
                    onLearnMore={handleLearnMore} 
                  />
                </Suspense>
              } 
            />
            <Route 
              path="/create/:type" 
              element={
                <Suspense fallback={<RouteLoading route="/create" />}>
                  <LazyDocumentCreator type="enhanced" />
                </Suspense>
              } 
            />
            <Route 
              path="/create/:type/premium" 
              element={
                <Suspense fallback={<RouteLoading route="/create" />}>
                  <LazyDocumentCreator type="premium" />
                </Suspense>
              } 
            />
            <Route 
              path="/edit/:id" 
              element={
                <Suspense fallback={<RouteLoading route="/edit" />}>
                  <DocumentEditor />
                </Suspense>
              } 
            />
            <Route 
              path="/preview/:id" 
              element={
                <Suspense fallback={<RouteLoading route="/preview" />}>
                  <DocumentPreview />
                </Suspense>
              } 
            />
            {/* Catch-all route for 404 */}
            <Route 
              path="*" 
              element={
                <div className="min-h-screen flex items-center justify-center">
                  <div className="text-center">
                    <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                      Page Not Found
                    </h1>
                    <p className="text-gray-600 dark:text-gray-400 mb-8">
                      The page you're looking for doesn't exist.
                    </p>
                    <button
                      onClick={() => navigate('/')}
                      className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      Go Home
                    </button>
                  </div>
                </div>
              } 
            />
          </Routes>
        </main>
        
        {/* Toast notifications */}
        <Toaster />
      </div>
    </ErrorBoundary>
  )
}

// Main App component with providers
function App() {
  const [isLoading, setIsLoading] = useState(true)

  // Simulate initial app loading
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false)
    }, 1000)

    return () => clearTimeout(timer)
  }, [])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-blue-900">
        <EnhancedLoading 
          message="Ontario Wills & POA App"
          submessage="Loading your legal document platform..."
          type="legal"
          size="large"
        />
      </div>
    )
  }

  return (
    <ErrorBoundary>
      <ThemeProvider>
        <Router basename={config.githubPages.basePath}>
          <AppContent />
        </Router>
      </ThemeProvider>
    </ErrorBoundary>
  )
}

export default App
