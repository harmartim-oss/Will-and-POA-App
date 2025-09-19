import React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '../ui/button';

const PageHeader = ({ 
  title, 
  description, 
  children,
  actions,
  breadcrumbs,
  className,
  ...props 
}) => {
  return (
    <div 
      className={cn(
        "mb-8 space-y-4 border-b border-gray-200 dark:border-gray-700 pb-6",
        className
      )}
      {...props}
    >
      {/* Breadcrumbs */}
      {breadcrumbs && (
        <nav aria-label="Breadcrumb" className="flex" role="navigation">
          <ol className="flex items-center space-x-2 text-sm">
            {breadcrumbs.map((crumb, index) => (
              <li key={index} className="flex items-center">
                {index > 0 && (
                  <span className="mx-2 text-gray-400 dark:text-gray-500">/</span>
                )}
                {crumb.href ? (
                  <a
                    href={crumb.href}
                    className={cn(
                      "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300",
                      "transition-colors duration-200",
                      "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-sm"
                    )}
                  >
                    {crumb.label}
                  </a>
                ) : (
                  <span className="text-gray-900 dark:text-white font-medium">
                    {crumb.label}
                  </span>
                )}
              </li>
            ))}
          </ol>
        </nav>
      )}

      {/* Main header content */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
        <div className="flex-1 min-w-0">
          {/* Title */}
          <h1 className={cn(
            "text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white",
            "leading-tight tracking-tight"
          )}>
            {title}
          </h1>
          
          {/* Description */}
          {description && (
            <p className="mt-2 text-base text-gray-600 dark:text-gray-400 max-w-2xl">
              {description}
            </p>
          )}
          
          {/* Custom content */}
          {children}
        </div>

        {/* Actions */}
        {actions && (
          <div className="flex-shrink-0">
            <div className="flex items-center space-x-3">
              {Array.isArray(actions) ? (
                actions.map((action, index) => (
                  <div key={index}>{action}</div>
                ))
              ) : (
                actions
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// Helper component for common action patterns
PageHeader.ActionButton = ({ variant = "default", children, ...props }) => (
  <Button variant={variant} {...props}>
    {children}
  </Button>
);

// Helper component for status badges
PageHeader.Status = ({ children, variant = "secondary", className, ...props }) => {
  const variants = {
    success: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400",
    warning: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400",
    danger: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400",
    secondary: "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300"
  };

  return (
    <span 
      className={cn(
        "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
};

// Helper component for meta information
PageHeader.Meta = ({ children, className, ...props }) => (
  <div 
    className={cn(
      "mt-3 flex flex-wrap items-center gap-4 text-sm text-gray-500 dark:text-gray-400",
      className
    )}
    {...props}
  >
    {children}
  </div>
);

export default PageHeader;