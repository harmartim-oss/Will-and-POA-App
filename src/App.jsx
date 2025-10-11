import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom'
import { ThemeProvider } from './components/ThemeContext'
import ErrorBoundary from './components/ErrorBoundary'
import LandingPage from './components/LandingPage'
import EnhancedDocumentCreator from './components/EnhancedDocumentCreator'
import DocumentPreview from './components/DocumentPreview'
import { config } from './config/environment'
import { Toaster } from './components/ui/toaster'

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
            <main 
              id="main" 
              role="main" 
              className="focus:outline-none"
            >
              <ErrorBoundary>
                <Routes>
                  <Route path="/" element={<LandingPage />} />
                  <Route path="/create/:type" element={<EnhancedDocumentCreator />} />
                  <Route path="/preview/:id" element={<DocumentPreview />} />
                  <Route path="*" element={<LandingPage />} />
                </Routes>
              </ErrorBoundary>
            </main>
            <Toaster />
          </div>
        </Router>
      </ThemeProvider>
    </ErrorBoundary>
  )
}

export default App