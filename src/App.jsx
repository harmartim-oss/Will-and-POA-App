import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom'
import { Toaster } from './components/ui/toaster'
import { ThemeProvider } from './components/ThemeContext'
import AppLayout from './components/layout/AppLayout'
import ModernLandingPage from './components/ModernLandingPage'
import DocumentCreator from './components/DocumentCreator'
import DocumentEditor from './components/DocumentEditor'
import DocumentPreview from './components/DocumentPreview'
import ResearchPage from './components/ResearchPage'
import HelpPage from './components/HelpPage'
import { config } from './config/environment'

function App() {
  return (
    <ThemeProvider>
      <Router basename={config.githubPages.basePath}>
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
    <AppLayout>
      <Routes>
        <Route path="/" element={<ModernLandingPage onGetStarted={handleGetStarted} onLearnMore={handleLearnMore} />} />
        <Route path="/create/:type" element={<DocumentCreator />} />
        <Route path="/edit/:id" element={<DocumentEditor />} />
        <Route path="/preview/:id" element={<DocumentPreview />} />
        <Route path="/research" element={<ResearchPage />} />
        <Route path="/help" element={<HelpPage />} />
      </Routes>
      <Toaster />
    </AppLayout>
  )
}

export default App