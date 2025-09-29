import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './components/ThemeContext'
import SimpleDemoShowcase from './components/SimpleDemoShowcase'
import { config } from './config/environment'

function App() {
  return (
    <ThemeProvider>
      <Router basename={config.githubPages.basePath}>
        <a href="#main" className="skip-link">Skip to main content</a>
        <main id="main" role="main" className="block focus:outline-none">
          <Routes>
            <Route path="/" element={<SimpleDemoShowcase />} />
            <Route path="*" element={<SimpleDemoShowcase />} />
          </Routes>
        </main>
      </Router>
    </ThemeProvider>
  )
}

export default App