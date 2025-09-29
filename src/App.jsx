import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './components/ThemeContext'
import ErrorBoundary from './components/ErrorBoundary'
import SimpleDemoShowcase from './components/SimpleDemoShowcase'
import { config } from './config/environment'

function App() {
  // Enhanced logging for debugging
  console.log('🔧 App component initializing...', {
    basePath: config.githubPages.basePath,
    isGitHubPages: config.isGitHubPages,
    isDevelopment: config.isDevelopment,
    isProduction: config.isProduction,
    demoMode: config.githubPages.demoMode,
    apiBaseUrl: config.apiBaseUrl,
    features: config.features
  });

  return (
    <ErrorBoundary>
      <ThemeProvider>
        <Router basename={config.githubPages.basePath}>
          <a href="#main" className="skip-link">Skip to main content</a>
          <main id="main" role="main" className="block focus:outline-none">
            <ErrorBoundary>
              <Routes>
                <Route path="/" element={<SimpleDemoShowcase />} />
                <Route path="*" element={<SimpleDemoShowcase />} />
              </Routes>
            </ErrorBoundary>
          </main>
        </Router>
      </ThemeProvider>
    </ErrorBoundary>
  )
}

export default App