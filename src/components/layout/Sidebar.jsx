import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  Home, 
  FileText, 
  Users, 
  Scale, 
  BookOpen, 
  Settings, 
  HelpCircle,
  X,
  Plus,
  Eye,
  Edit
} from 'lucide-react';
import { Button } from '../ui/button';
import { cn } from '@/lib/utils';

const Sidebar = ({ isOpen, onClose }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const navigationSections = [
    {
      title: 'Overview',
      items: [
        {
          name: 'Home',
          href: '/',
          icon: Home,
          description: 'Return to main page'
        }
      ]
    },
    {
      title: 'Documents',
      items: [
        {
          name: 'Create Will',
          href: '/create/will',
          icon: Scale,
          description: 'Create a new will document'
        },
        {
          name: 'Create POA',
          href: '/create/poa',
          icon: Users,
          description: 'Create power of attorney'
        }
      ]
    },
    {
      title: 'Research & Help',
      items: [
        {
          name: 'Legal Research',
          href: '/research',
          icon: BookOpen,
          description: 'Browse legal resources'
        },
        {
          name: 'Help & Support',
          href: '/help',
          icon: HelpCircle,
          description: 'Get assistance and FAQs'
        }
      ]
    }
  ];

  const handleNavigation = (href) => {
    navigate(href);
    onClose();
  };

  const isActiveRoute = (href) => {
    if (href === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(href);
  };

  return (
    <>
      {/* Desktop sidebar */}
      <div className={cn(
        "hidden lg:flex lg:w-64 lg:flex-col lg:fixed lg:inset-y-0",
        "bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700",
        "transition-colors duration-200"
      )}>
        <SidebarContent 
          navigationSections={navigationSections}
          handleNavigation={handleNavigation}
          isActiveRoute={isActiveRoute}
          onClose={onClose}
          showCloseButton={false}
        />
      </div>

      {/* Mobile sidebar */}
      <div className={cn(
        "lg:hidden fixed inset-y-0 left-0 z-50 w-64 transform transition-transform duration-300 ease-in-out",
        isOpen ? "translate-x-0" : "-translate-x-full",
        "bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700"
      )}>
        <SidebarContent 
          navigationSections={navigationSections}
          handleNavigation={handleNavigation}
          isActiveRoute={isActiveRoute}
          onClose={onClose}
          showCloseButton={true}
        />
      </div>
    </>
  );
};

const SidebarContent = ({ 
  navigationSections, 
  handleNavigation, 
  isActiveRoute, 
  onClose, 
  showCloseButton 
}) => {
  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between h-16 px-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 dark:bg-blue-500">
            <Scale className="h-5 w-5 text-white" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-gray-900 dark:text-white">
              Ontario Wills
            </h2>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Legal Documents
            </p>
          </div>
        </div>
        
        {showCloseButton && (
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
            aria-label="Close menu"
          >
            <X className="h-5 w-5" />
          </Button>
        )}
      </div>

      {/* Navigation */}
      <nav 
        role="navigation" 
        aria-label="Main navigation"
        className="flex-1 px-4 py-6 space-y-8 overflow-y-auto"
      >
        {navigationSections.map((section) => (
          <div key={section.title}>
            <h3 className="px-3 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              {section.title}
            </h3>
            <div className="mt-3 space-y-1">
              {section.items.map((item) => {
                const Icon = item.icon;
                const isActive = isActiveRoute(item.href);
                
                return (
                  <button
                    key={item.name}
                    onClick={() => handleNavigation(item.href)}
                    className={cn(
                      "group flex w-full items-center rounded-md px-3 py-2 text-sm font-medium transition-colors duration-200",
                      "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
                      isActive
                        ? "bg-blue-50 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300"
                        : "text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
                    )}
                    aria-current={isActive ? 'page' : undefined}
                    title={item.description}
                  >
                    <Icon
                      className={cn(
                        "mr-3 h-5 w-5 flex-shrink-0 transition-colors duration-200",
                        isActive
                          ? "text-blue-600 dark:text-blue-400"
                          : "text-gray-400 dark:text-gray-500 group-hover:text-gray-500 dark:group-hover:text-gray-400"
                      )}
                      aria-hidden="true"
                    />
                    <span className="flex-1 text-left">{item.name}</span>
                    {isActive && (
                      <div className="w-1 h-1 bg-blue-600 dark:bg-blue-400 rounded-full" />
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      {/* Quick actions */}
      <div className="px-4 py-4 border-t border-gray-200 dark:border-gray-700 space-y-2">
        <h4 className="px-3 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
          Quick Actions
        </h4>
        <Button
          variant="outline"
          size="sm"
          onClick={() => handleNavigation('/create/will')}
          className="w-full justify-start"
        >
          <Plus className="mr-2 h-4 w-4" />
          Create Will
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() => handleNavigation('/create/poa')}
          className="w-full justify-start"
        >
          <Plus className="mr-2 h-4 w-4" />
          Create POA
        </Button>
      </div>
    </div>
  );
};

export default Sidebar;