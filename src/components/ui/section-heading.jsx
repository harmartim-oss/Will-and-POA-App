import React from 'react';
import { cn } from '@/lib/utils';

// SectionHeading component for consistent section titles and descriptions
const SectionHeading = ({ 
  title,
  description,
  level = 2,
  className,
  children,
  actions,
  border = false,
  spacing = "default",
  ...props 
}) => {
  const Component = `h${level}`;
  
  const levelClasses = {
    1: "text-3xl font-bold tracking-tight",
    2: "text-2xl font-bold tracking-tight",
    3: "text-xl font-semibold tracking-tight",
    4: "text-lg font-semibold tracking-tight",
    5: "text-base font-semibold tracking-tight",
    6: "text-sm font-semibold tracking-tight",
  };

  const spacingClasses = {
    tight: "mb-4",
    default: "mb-6",
    loose: "mb-8",
  };

  return (
    <div
      className={cn(
        spacingClasses[spacing],
        border && "border-b border-gray-200 dark:border-gray-700 pb-4",
        className
      )}
      {...props}
    >
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex-1 min-w-0">
          <Component className={cn(
            levelClasses[level] || levelClasses[2],
            "text-gray-900 dark:text-gray-100",
            description ? "mb-2" : ""
          )}>
            {title}
          </Component>
          
          {description && (
            <p className="text-gray-600 dark:text-gray-400 max-w-2xl">
              {description}
            </p>
          )}
          
          {children}
        </div>

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

// Helper components for metadata and status
SectionHeading.Meta = ({ children, className, ...props }) => (
  <div 
    className={cn(
      "mt-2 flex flex-wrap items-center gap-4 text-sm text-gray-500 dark:text-gray-400",
      className
    )}
    {...props}
  >
    {children}
  </div>
);

SectionHeading.Badge = ({ children, variant = "secondary", className, ...props }) => {
  const variants = {
    primary: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400",
    secondary: "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300",
    success: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400",
    warning: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400",
    danger: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400",
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

export { SectionHeading };