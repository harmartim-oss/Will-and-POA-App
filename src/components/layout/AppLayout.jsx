import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { cn } from '@/lib/utils';
import Header from './Header';
import Sidebar from './Sidebar';
import { useTheme } from '../ThemeContext';

const AppLayout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const { theme } = useTheme();
  
  // Don't show layout on landing page
  const isLandingPage = location.pathname === '/';
  
  if (isLandingPage) {
    return (
      <>
        {/* Skip link for accessibility */}
        <a
          href="#main-content"
          className="skip-link"
          tabIndex={0}
        >
          Skip to main content
        </a>
        <main id="main-content" role="main" className="focus:outline-none" tabIndex={-1}>
          {children}
        </main>
      </>
    );
  }

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* Skip link for accessibility */}
      <a
        href="#main-content"
        className="skip-link"
        tabIndex={0}
      >
        Skip to main content
      </a>

      {/* Sidebar */}
      <Sidebar 
        isOpen={sidebarOpen} 
        onClose={() => setSidebarOpen(false)}
      />

      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-gray-600 bg-opacity-75 lg:hidden"
          onClick={() => setSidebarOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Main content area */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Header */}
        <Header onMenuClick={() => setSidebarOpen(true)} />

        {/* Main content */}
        <main 
          id="main-content" 
          role="main" 
          className={cn(
            "flex-1 overflow-y-auto focus:outline-none",
            "bg-white dark:bg-gray-900",
            "transition-colors duration-200"
          )}
          tabIndex={-1}
        >
          <div className="py-6">
            <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
              {children}
            </div>
          </div>
        </main>

        {/* Footer placeholder */}
        <footer 
          role="contentinfo"
          className={cn(
            "bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700",
            "px-4 py-4 sm:px-6 lg:px-8"
          )}
        >
          <div className="max-w-7xl mx-auto">
            <div className="flex flex-col sm:flex-row justify-between items-center space-y-2 sm:space-y-0">
              <div className="text-sm text-gray-500 dark:text-gray-400">
                <span>© 2024 Ontario Wills & POA Creator.</span>
                <span className="ml-2">Professional legal document assistance.</span>
              </div>
              <div className="text-xs text-gray-400 dark:text-gray-500">
                <span>v3.0.0</span>
                <span className="mx-2">•</span>
                <span>Legal disclaimers coming soon</span>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default AppLayout;