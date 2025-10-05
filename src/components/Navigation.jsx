import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Menu, 
  X, 
  FileText, 
  Home, 
  Info, 
  Phone, 
  Moon, 
  Sun, 
  ChevronLeft,
  ChevronRight,
  Settings,
  HelpCircle,
  BookOpen,
  Bell,
  Search
} from 'lucide-react';
import { useTheme } from './ThemeContext';

const Navigation = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();

  const navLinks = [
    { path: '/', label: 'Dashboard', icon: Home },
    { path: '/about', label: 'About', icon: Info },
    { path: '/contact', label: 'Support', icon: Phone },
    { path: '/docs', label: 'Documentation', icon: BookOpen },
    { path: '/settings', label: 'Settings', icon: Settings }
  ];

  const isActive = (path) => {
    return location.pathname === path;
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const toggleMobileSidebar = () => {
    setIsMobileSidebarOpen(!isMobileSidebarOpen);
  };

  return (
    <>
      {/* Top Bar for Mobile and Notifications - Enhanced */}
      <div className="fixed top-0 left-0 right-0 h-16 bg-white/95 dark:bg-gray-900/95 backdrop-blur-md border-b-2 border-gray-200 dark:border-gray-700 z-50 lg:hidden shadow-md">
        <div className="flex items-center justify-between h-full px-4">
          <button
            onClick={toggleMobileSidebar}
            className="p-2.5 rounded-xl text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50 dark:hover:from-blue-900/20 dark:hover:to-purple-900/20 transition-all hover:scale-110"
            aria-label="Toggle menu"
          >
            <Menu className="h-6 w-6" />
          </button>
          
          <Link to="/" className="flex items-center space-x-2">
            <div className="p-2 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 rounded-xl shadow-lg">
              <FileText className="h-5 w-5 text-white" />
            </div>
            <span className="text-lg font-extrabold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Ontario Wills
            </span>
          </Link>

          <button
            onClick={toggleTheme}
            className="p-2.5 rounded-xl text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-yellow-50 hover:to-orange-50 dark:hover:from-yellow-900/20 dark:hover:to-orange-900/20 transition-all hover:scale-110"
            aria-label="Toggle theme"
          >
            {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {/* Desktop Sidebar - Enhanced with modern styling */}
      <aside
        className={`hidden lg:flex flex-col fixed left-0 top-0 h-screen bg-white/95 dark:bg-gray-900/95 backdrop-blur-md border-r border-gray-200 dark:border-gray-700 shadow-xl transition-all duration-300 z-40 ${
          isSidebarOpen ? 'w-64' : 'w-20'
        }`}
      >
        {/* Sidebar Header */}
        <div className="flex items-center justify-between p-4 border-b-2 border-gray-200 dark:border-gray-700">
          {isSidebarOpen && (
            <Link to="/" className="flex items-center space-x-2 group">
              <div className="p-2 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 rounded-xl group-hover:scale-110 transition-transform duration-200 shadow-lg">
                <FileText className="h-5 w-5 text-white" />
              </div>
              <span className="text-lg font-extrabold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Ontario Wills
              </span>
            </Link>
          )}
          {!isSidebarOpen && (
            <div className="mx-auto p-2 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 rounded-xl shadow-lg">
              <FileText className="h-5 w-5 text-white" />
            </div>
          )}
          <button
            onClick={toggleSidebar}
            className="p-2 rounded-xl text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-all hover:scale-110"
            aria-label="Toggle sidebar"
          >
            {isSidebarOpen ? <ChevronLeft className="h-5 w-5" /> : <ChevronRight className="h-5 w-5" />}
          </button>
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 overflow-y-auto py-5">
          <div className="space-y-2 px-3">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`group flex items-center space-x-3 px-4 py-3.5 rounded-xl text-sm font-semibold transition-all duration-200 ${
                  isActive(link.path)
                    ? 'bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 text-white shadow-lg scale-105'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50 dark:hover:from-blue-900/20 dark:hover:to-purple-900/20 hover:scale-105'
                } ${!isSidebarOpen && 'justify-center'}`}
                title={!isSidebarOpen ? link.label : ''}
              >
                <link.icon className={`h-5 w-5 flex-shrink-0 ${isActive(link.path) ? '' : 'group-hover:scale-110 transition-transform'}`} />
                {isSidebarOpen && <span>{link.label}</span>}
              </Link>
            ))}
          </div>
        </nav>

        {/* Sidebar Footer */}
        <div className="border-t-2 border-gray-200 dark:border-gray-700 p-3 space-y-2">
          <button
            onClick={toggleTheme}
            className={`group flex items-center space-x-3 w-full px-4 py-3.5 rounded-xl text-sm font-semibold text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-yellow-50 hover:to-orange-50 dark:hover:from-yellow-900/20 dark:hover:to-orange-900/20 transition-all hover:scale-105 ${
              !isSidebarOpen && 'justify-center'
            }`}
            title={!isSidebarOpen ? 'Toggle theme' : ''}
          >
            {theme === 'dark' ? <Sun className="h-5 w-5 group-hover:rotate-180 transition-transform duration-500" /> : <Moon className="h-5 w-5 group-hover:rotate-12 transition-transform" />}
            {isSidebarOpen && <span>{theme === 'dark' ? 'Light Mode' : 'Dark Mode'}</span>}
          </button>
          
          <button
            className={`group flex items-center space-x-3 w-full px-4 py-3.5 rounded-xl text-sm font-semibold text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-green-50 hover:to-emerald-50 dark:hover:from-green-900/20 dark:hover:to-emerald-900/20 transition-all hover:scale-105 ${
              !isSidebarOpen && 'justify-center'
            }`}
            title={!isSidebarOpen ? 'Help' : ''}
          >
            <HelpCircle className="h-5 w-5 group-hover:scale-110 transition-transform" />
            {isSidebarOpen && <span>Help & Support</span>}
          </button>
        </div>
      </aside>

      {/* Mobile Sidebar - Enhanced */}
      {isMobileSidebarOpen && (
        <>
          <div
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden animate-in fade-in duration-200"
            onClick={toggleMobileSidebar}
          ></div>
          <aside className="fixed left-0 top-0 h-screen w-64 bg-white/95 dark:bg-gray-900/95 backdrop-blur-md border-r-2 border-gray-200 dark:border-gray-700 z-50 lg:hidden transform transition-transform duration-300 shadow-2xl">
            {/* Mobile Sidebar Header */}
            <div className="flex items-center justify-between p-4 border-b-2 border-gray-200 dark:border-gray-700">
              <Link to="/" className="flex items-center space-x-2">
                <div className="p-2 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 rounded-xl shadow-lg">
                  <FileText className="h-5 w-5 text-white" />
                </div>
                <span className="text-lg font-extrabold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Ontario Wills
                </span>
              </Link>
              <button
                onClick={toggleMobileSidebar}
                className="p-2 rounded-xl text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-all hover:scale-110"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Mobile Navigation Links */}
            <nav className="flex-1 overflow-y-auto py-5">
              <div className="space-y-2 px-3">
                {navLinks.map((link) => (
                  <Link
                    key={link.path}
                    to={link.path}
                    onClick={toggleMobileSidebar}
                    className={`group flex items-center space-x-3 px-4 py-3.5 rounded-xl text-sm font-semibold transition-all duration-200 ${
                      isActive(link.path)
                        ? 'bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 text-white shadow-lg scale-105'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50 dark:hover:from-blue-900/20 dark:hover:to-purple-900/20 hover:scale-105'
                    }`}
                  >
                    <link.icon className={`h-5 w-5 ${isActive(link.path) ? '' : 'group-hover:scale-110 transition-transform'}`} />
                    <span>{link.label}</span>
                  </Link>
                ))}
              </div>
            </nav>

            {/* Mobile Sidebar Footer */}
            <div className="border-t-2 border-gray-200 dark:border-gray-700 p-3 space-y-2">
              <button
                onClick={toggleTheme}
                className="group flex items-center space-x-3 w-full px-4 py-3.5 rounded-xl text-sm font-semibold text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-yellow-50 hover:to-orange-50 dark:hover:from-yellow-900/20 dark:hover:to-orange-900/20 transition-all hover:scale-105"
              >
                {theme === 'dark' ? <Sun className="h-5 w-5 group-hover:rotate-180 transition-transform duration-500" /> : <Moon className="h-5 w-5 group-hover:rotate-12 transition-transform" />}
                <span>{theme === 'dark' ? 'Light Mode' : 'Dark Mode'}</span>
              </button>
              
              <button className="group flex items-center space-x-3 w-full px-4 py-3.5 rounded-xl text-sm font-semibold text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-green-50 hover:to-emerald-50 dark:hover:from-green-900/20 dark:hover:to-emerald-900/20 transition-all hover:scale-105">
                <HelpCircle className="h-5 w-5 group-hover:scale-110 transition-transform" />
                <span>Help & Support</span>
              </button>
            </div>
          </aside>
        </>
      )}

      {/* Spacer for desktop sidebar */}
      <div className={`hidden lg:block transition-all duration-300 ${isSidebarOpen ? 'w-64' : 'w-20'}`}></div>
    </>
  );
};

export default Navigation;
