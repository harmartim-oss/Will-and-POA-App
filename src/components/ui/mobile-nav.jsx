import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X, Home, FileText, Shield, Users, Phone, Mail, Sun, Moon } from 'lucide-react';
import { Button } from './button';
import { useTheme } from '../ThemeContext';
import { cn } from '../../lib/utils';

const MobileNav = ({ 
  isOpen, 
  onToggle, 
  onNavigate,
  currentPath = '/',
  className 
}) => {
  const { theme, toggleTheme, isDark } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const navigationItems = [
    {
      icon: Home,
      label: 'Home',
      path: '/',
      description: 'Return to homepage'
    },
    {
      icon: FileText,
      label: 'Create Will',
      path: '/create/will',
      description: 'Create a Last Will & Testament'
    },
    {
      icon: Shield,
      label: 'Power of Attorney',
      path: '/create/poa',
      description: 'Create Power of Attorney documents'
    },
    {
      icon: Users,
      label: 'About',
      path: '/about',
      description: 'Learn more about our service'
    }
  ];

  const contactItems = [
    {
      icon: Phone,
      label: '1-800-LEGAL-AI',
      href: 'tel:1-800-534-2524',
      description: 'Call for support'
    },
    {
      icon: Mail,
      label: 'support@ontariowills.ai',
      href: 'mailto:support@ontariowills.ai',
      description: 'Email us'
    }
  ];

  const handleNavigation = (path) => {
    onNavigate(path);
    onToggle();
  };

  const handleExternalLink = (href) => {
    window.open(href, '_blank', 'noopener,noreferrer');
  };

  // Prevent body scroll when menu is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  if (!mounted) return null;

  return (
    <>
      {/* Mobile menu button */}
      <Button
        variant="ghost"
        size="sm"
        onClick={onToggle}
        className={cn(
          "md:hidden p-2 text-white hover:bg-white/10 rounded-lg",
          className
        )}
        aria-label={isOpen ? 'Close menu' : 'Open menu'}
        aria-expanded={isOpen}
      >
        <AnimatePresence mode="wait">
          {isOpen ? (
            <motion.div
              key="close"
              initial={{ rotate: -90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: 90, opacity: 0 }}
              transition={{ duration: 0.2 }}
            >
              <X className="h-6 w-6" />
            </motion.div>
          ) : (
            <motion.div
              key="menu"
              initial={{ rotate: 90, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: -90, opacity: 0 }}
              transition={{ duration: 0.2 }}
            >
              <Menu className="h-6 w-6" />
            </motion.div>
          )}
        </AnimatePresence>
      </Button>

      {/* Mobile menu overlay */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 md:hidden"
              onClick={onToggle}
            />

            {/* Menu panel */}
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="fixed top-0 right-0 bottom-0 w-80 max-w-[85vw] bg-white dark:bg-gray-900 shadow-2xl z-50 md:hidden"
            >
              <div className="flex flex-col h-full">
                {/* Header */}
                <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
                      <FileText className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                    </div>
                    <div>
                      <h2 className="font-semibold text-gray-900 dark:text-white">
                        Ontario Legal
                      </h2>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Document Creator
                      </p>
                    </div>
                  </div>
                  
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={toggleTheme}
                    className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg"
                    aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
                  >
                    {isDark ? (
                      <Sun className="h-5 w-5 text-gray-600 dark:text-gray-400" />
                    ) : (
                      <Moon className="h-5 w-5 text-gray-600 dark:text-gray-400" />
                    )}
                  </Button>
                </div>

                {/* Navigation */}
                <div className="flex-1 overflow-y-auto py-6">
                  <nav className="space-y-2 px-6">
                    <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3">
                      Navigation
                    </h3>
                    
                    {navigationItems.map((item, index) => {
                      const Icon = item.icon;
                      const isActive = currentPath === item.path;
                      
                      return (
                        <motion.button
                          key={item.path}
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: index * 0.1 }}
                          onClick={() => handleNavigation(item.path)}
                          className={cn(
                            "w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-left transition-all duration-200",
                            isActive
                              ? "bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800"
                              : "text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
                          )}
                        >
                          <div className={cn(
                            "p-2 rounded-lg transition-colors",
                            isActive
                              ? "bg-blue-100 dark:bg-blue-800"
                              : "bg-gray-100 dark:bg-gray-700"
                          )}>
                            <Icon className="h-5 w-5" />
                          </div>
                          <div className="flex-1">
                            <div className="font-medium">{item.label}</div>
                            <div className="text-sm text-gray-500 dark:text-gray-400">
                              {item.description}
                            </div>
                          </div>
                        </motion.button>
                      );
                    })}
                  </nav>

                  {/* Contact section */}
                  <div className="mt-8 px-6">
                    <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3">
                      Contact
                    </h3>
                    
                    <div className="space-y-2">
                      {contactItems.map((item, index) => {
                        const Icon = item.icon;
                        
                        return (
                          <motion.button
                            key={item.href}
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: (navigationItems.length + index) * 0.1 }}
                            onClick={() => handleExternalLink(item.href)}
                            className="w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-left text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 transition-all duration-200"
                          >
                            <div className="p-2 bg-gray-100 dark:bg-gray-700 rounded-lg">
                              <Icon className="h-5 w-5" />
                            </div>
                            <div className="flex-1">
                              <div className="font-medium">{item.label}</div>
                              <div className="text-sm text-gray-500 dark:text-gray-400">
                                {item.description}
                              </div>
                            </div>
                          </motion.button>
                        );
                      })}
                    </div>
                  </div>
                </div>

                {/* Footer */}
                <div className="p-6 border-t border-gray-200 dark:border-gray-700">
                  <div className="text-center">
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      © 2024 Ontario Legal Docs
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                      Professional legal document creation
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
};

export default MobileNav;
