import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from './components/ui/toaster'
import LandingPage from './components/LandingPage'
import DocumentCreator from './components/DocumentCreator'
import DocumentEditor from './components/DocumentEditor'
import DocumentPreview from './components/DocumentPreview'
import { config } from './config/environment'

function App() {
  return (
    <Router basename={config.githubPages.basePath}>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/create/:type" element={<DocumentCreator />} />
          <Route path="/edit/:id" element={<DocumentEditor />} />
          <Route path="/preview/:id" element={<DocumentPreview />} />
        </Routes>
        <Toaster />
      </div>
    </Router>
  )
}

export default App