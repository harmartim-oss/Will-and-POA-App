import React from 'react';
import { cn } from '@/lib/utils';
import { Button } from './button';

// ActionBar component for consistent action button layouts
const ActionBar = ({ 
  children, 
  className, 
  align = "right",
  spacing = "default",
  ...props 
}) => {
  const alignClasses = {
    left: "justify-start",
    center: "justify-center", 
    right: "justify-end",
    between: "justify-between",
    around: "justify-around",
  };

  const spacingClasses = {
    tight: "space-x-2",
    default: "space-x-3",
    loose: "space-x-4",
  };

  return (
    <div
      className={cn(
        "flex items-center",
        alignClasses[align],
        spacingClasses[spacing],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

// Helper components for common ActionBar patterns
ActionBar.Primary = ({ children, ...props }) => (
  <Button variant="primary" {...props}>
    {children}
  </Button>
);

ActionBar.Secondary = ({ children, ...props }) => (
  <Button variant="secondary" {...props}>
    {children}
  </Button>
);

ActionBar.Danger = ({ children, ...props }) => (
  <Button variant="danger" {...props}>
    {children}
  </Button>
);

ActionBar.Ghost = ({ children, ...props }) => (
  <Button variant="ghost" {...props}>
    {children}
  </Button>
);

export { ActionBar };