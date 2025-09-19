import React from 'react';
import { cn } from '@/lib/utils';
import { Button } from './button';

// EmptyState component for consistent empty state displays
const EmptyState = ({ 
  icon: Icon,
  title,
  description,
  action,
  className,
  size = "default",
  ...props 
}) => {
  const sizeClasses = {
    sm: {
      container: "py-8",
      icon: "h-12 w-12",
      title: "text-lg",
      description: "text-sm",
    },
    default: {
      container: "py-12",
      icon: "h-16 w-16",
      title: "text-xl",
      description: "text-base",
    },
    lg: {
      container: "py-16",
      icon: "h-20 w-20",
      title: "text-2xl",
      description: "text-lg",
    },
  };

  const currentSize = sizeClasses[size] || sizeClasses.default;

  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center text-center",
        currentSize.container,
        className
      )}
      {...props}
    >
      {Icon && (
        <div className={cn(
          "flex items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800 mb-4",
          "text-gray-400 dark:text-gray-500",
          currentSize.icon,
          "p-4"
        )}>
          <Icon className={cn(currentSize.icon)} />
        </div>
      )}
      
      {title && (
        <h3 className={cn(
          "font-semibold text-gray-900 dark:text-gray-100 mb-2",
          currentSize.title
        )}>
          {title}
        </h3>
      )}
      
      {description && (
        <p className={cn(
          "text-gray-600 dark:text-gray-400 max-w-md mx-auto mb-6",
          currentSize.description
        )}>
          {description}
        </p>
      )}
      
      {action && (
        <div className="flex flex-col sm:flex-row gap-3">
          {Array.isArray(action) ? (
            action.map((item, index) => (
              <div key={index}>{item}</div>
            ))
          ) : (
            action
          )}
        </div>
      )}
    </div>
  );
};

// Helper components for common EmptyState patterns
EmptyState.Action = ({ children, ...props }) => (
  <Button variant="primary" {...props}>
    {children}
  </Button>
);

EmptyState.SecondaryAction = ({ children, ...props }) => (
  <Button variant="outline" {...props}>
    {children}
  </Button>
);

export { EmptyState };