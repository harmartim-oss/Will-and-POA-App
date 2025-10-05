import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './components/ThemeContext'
import ErrorBoundary from './components/ErrorBoundary'
import Navigation from './components/Navigation'
import Footer from './components/Footer'
import SimpleDemoShowcase from './components/SimpleDemoShowcase'
import { config } from './config/environment'

function App() {
  // Enhanced logging for debugging (only in development)
  if (config.isDevelopment) {
    console.log('🔧 App component initializing...', {
      basePath: config.githubPages.basePath,
      isGitHubPages: config.isGitHubPages,
      isDevelopment: config.isDevelopment,
      isProduction: config.isProduction,
      demoMode: config.githubPages.demoMode,
      apiBaseUrl: config.apiBaseUrl,
      features: config.features
    });
  }

  return (
    <ErrorBoundary>
      <ThemeProvider>
        <Router basename={config.githubPages.basePath}>
          <div className="min-h-screen">
            <a href="#main" className="skip-link">Skip to main content</a>
            <Navigation />
            <main 
              id="main" 
              role="main" 
              className="pt-16 lg:pt-0 focus:outline-none"
            >
              <ErrorBoundary>
                <Routes>
                  <Route path="/" element={<SimpleDemoShowcase />} />
                  <Route path="/about" element={<SimpleDemoShowcase />} />
                  <Route path="/contact" element={<SimpleDemoShowcase />} />
                  <Route path="*" element={<SimpleDemoShowcase />} />
                </Routes>
              </ErrorBoundary>
            </main>
            <Footer />
          </div>
        </Router>
      </ThemeProvider>
    </ErrorBoundary>
  )
}

export default App