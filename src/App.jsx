import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom'
import { Toaster } from './components/ui/toaster'
import { ThemeProvider } from './components/ThemeContext'
import ModernLandingPage from './components/ModernLandingPage'
import DocumentCreator from './components/DocumentCreator'
import EnhancedDocumentCreator from './components/EnhancedDocumentCreator'
import DocumentEditor from './components/DocumentEditor'
import DocumentPreview from './components/DocumentPreview'
import DemoShowcase from './components/DemoShowcase'
import SolePractitionerDashboard from './components/SolePractitionerDashboard'
import { config } from './config/environment'

function App() {
  return (
    <ThemeProvider>
      <Router basename={config.githubPages.basePath}>
        <a href="#main" className="skip-link">Skip to main content</a>
        <AppContent />
      </Router>
    </ThemeProvider>
  )
}

function AppContent() {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    // Navigate to document selection or first document type
    navigate('/create/will');
  };

  const handleLearnMore = () => {
    // For now, scroll to features section or show modal
    const featuresSection = document.getElementById('features');
    if (featuresSection) {
      featuresSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-blue-900">
      <main id="main" role="main" className="block focus:outline-none">
        <Routes>
          <Route path="/" element={<DemoShowcase />} />
          <Route path="/landing" element={<ModernLandingPage onGetStarted={handleGetStarted} onLearnMore={handleLearnMore} />} />
          <Route path="/create/:type" element={<DocumentCreator />} />
          <Route path="/edit/:id" element={<DocumentEditor />} />
          <Route path="/preview/:id" element={<DocumentPreview />} />
          <Route path="/sole-practitioner" element={<SolePractitionerDashboard />} />
        </Routes>
      </main>
      <Toaster />
    </div>
  )
}

export default App