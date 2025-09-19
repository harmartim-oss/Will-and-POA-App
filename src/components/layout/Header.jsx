import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Menu, Moon, Sun, Scale, Home, ArrowLeft } from 'lucide-react';
import { Button } from '../ui/button';
import { useTheme } from '../ThemeContext';
import { cn } from '@/lib/utils';

const Header = ({ onMenuClick }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { theme, toggleTheme, isDark } = useTheme();

  const canGoBack = location.pathname !== '/' && location.pathname !== '/create/will' && location.pathname !== '/create/poa';

  const handleBackClick = () => {
    if (canGoBack) {
      navigate(-1);
    } else {
      navigate('/');
    }
  };

  const handleHomeClick = () => {
    navigate('/');
  };

  return (
    <header 
      role="banner"
      className={cn(
        "bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700",
        "transition-colors duration-200"
      )}
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 justify-between items-center">
          {/* Left section */}
          <div className="flex items-center space-x-4">
            {/* Mobile menu button */}
            <Button
              variant="ghost"
              size="sm"
              onClick={onMenuClick}
              className="lg:hidden"
              aria-label="Open main menu"
            >
              <Menu className="h-5 w-5" />
            </Button>

            {/* Back button */}
            {canGoBack && (
              <Button
                variant="ghost"
                size="sm"
                onClick={handleBackClick}
                aria-label="Go back"
                className="hidden sm:flex"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back
              </Button>
            )}

            {/* App branding */}
            <button
              onClick={handleHomeClick}
              className={cn(
                "flex items-center space-x-3 text-gray-900 dark:text-white",
                "hover:text-blue-600 dark:hover:text-blue-400",
                "transition-colors duration-200",
                "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
                "rounded-md px-2 py-1"
              )}
              aria-label="Go to home page"
            >
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 dark:bg-blue-500">
                <Scale className="h-5 w-5 text-white" />
              </div>
              <div className="hidden sm:block">
                <h1 className="text-lg font-semibold">Ontario Wills & POA</h1>
                <p className="text-xs text-gray-500 dark:text-gray-400 -mt-1">
                  Professional Legal Documents
                </p>
              </div>
            </button>
          </div>

          {/* Right section */}
          <div className="flex items-center space-x-4">
            {/* Home button (mobile) */}
            <Button
              variant="ghost"
              size="sm"
              onClick={handleHomeClick}
              className="sm:hidden"
              aria-label="Go to home page"
            >
              <Home className="h-5 w-5" />
            </Button>

            {/* Theme toggle */}
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleTheme}
              aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
              className="relative"
            >
              <div className="relative h-5 w-5">
                <Sun 
                  className={cn(
                    "absolute h-5 w-5 transition-all duration-300",
                    isDark ? "rotate-90 scale-0" : "rotate-0 scale-100"
                  )} 
                />
                <Moon 
                  className={cn(
                    "absolute h-5 w-5 transition-all duration-300",
                    isDark ? "rotate-0 scale-100" : "-rotate-90 scale-0"
                  )} 
                />
              </div>
            </Button>

            {/* User menu placeholder */}
            <div className="hidden md:flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
              <span>Guest User</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;