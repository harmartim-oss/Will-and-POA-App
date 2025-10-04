import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// Global error handlers for production debugging
window.addEventListener('error', (event) => {
  console.error('❌ Global error:', event.error);
  console.error('Error details:', {
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    stack: event.error?.stack
  });
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('❌ Unhandled promise rejection:', event.reason);
});

// Enhanced logging for production debugging
console.log('🚀 Application starting up...', {
  href: window.location.href,
  pathname: window.location.pathname,
  hostname: window.location.hostname,
  isGitHubPages: window.location.hostname.includes('github.io'),
  userAgent: navigator.userAgent,
  timestamp: new Date().toISOString(),
  NODE_ENV: import.meta.env.MODE,
  VITE_GITHUB_PAGES: import.meta.env.VITE_GITHUB_PAGES,
  base: import.meta.env.BASE_URL
});

// Check if running on correct path
if (window.location.hostname.includes('github.io') && !window.location.pathname.startsWith('/Will-and-POA-App')) {
  console.warn('⚠️ Incorrect base path detected. Expected /Will-and-POA-App/, got:', window.location.pathname);
}

try {
  const rootElement = document.getElementById('root');
  if (!rootElement) {
    throw new Error('Root element not found');
  }
  
  console.log('✅ Root element found, creating React root...');
  
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
  );
  
  console.log('✅ React app rendered successfully');
  
  // Remove initial loader with a small delay to ensure React has fully rendered
  setTimeout(() => {
    if (window.removeInitialLoader) {
      console.log('🔄 Using removeInitialLoader function');
      window.removeInitialLoader();
    }
    // Fallback: directly remove the loader if the function doesn't work
    const loader = document.getElementById('initial-loader');
    if (loader && loader.parentNode) {
      console.log('🔄 Removing initial loader');
      loader.remove();
      console.log('✅ Initial loader removed - app fully loaded');
    }
  }, 100);
} catch (error) {
  console.error('❌ Failed to initialize React app:', error);
  console.error('Stack trace:', error.stack);
  console.error('Environment at failure:', {
    location: window.location.href,
    baseUrl: import.meta.env.BASE_URL,
    mode: import.meta.env.MODE
  });
  
  // Fallback error display
  const rootElement = document.getElementById('root');
  if (rootElement) {
    rootElement.innerHTML = `
      <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 2rem; font-family: system-ui, -apple-system, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div style="max-width: 500px; text-align: center; background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
          <div style="font-size: 3rem; margin-bottom: 1rem;">⚠️</div>
          <h1 style="color: #dc2626; margin-bottom: 1rem;">Application Failed to Load</h1>
          <p style="color: #374151; margin-bottom: 1.5rem;">
            There was an error loading the Ontario Wills & Power of Attorney Creator. 
            Please check the browser console for details and try refreshing the page.
          </p>
          <button 
            onclick="window.location.reload()" 
            style="background: #3b82f6; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 6px; cursor: pointer; font-size: 1rem; margin-bottom: 1rem;">
            Reload Page
          </button>
          <div style="margin-top: 1rem; padding: 1rem; background: #f9fafb; border-radius: 6px; text-align: left; font-family: monospace; font-size: 0.875rem; color: #dc2626; word-break: break-word;">
            <strong>Error:</strong> ${error.message}<br/>
            <strong>Location:</strong> ${window.location.pathname}
          </div>
          <p style="margin-top: 1rem; font-size: 0.75rem; color: #6b7280;">
            If this persists, please open your browser's developer console (F12) for more details.
          </p>
        </div>
      </div>
    `;
  }
}