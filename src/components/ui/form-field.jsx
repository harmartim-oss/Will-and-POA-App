import React from 'react';
import { cn } from '@/lib/utils';
import { Label } from './label';

// FormField component for consistent form element spacing and layout
const FormField = ({ 
  children, 
  className, 
  spacing = "default",
  ...props 
}) => {
  const spacingClasses = {
    tight: "space-y-1",
    default: "space-y-2",
    loose: "space-y-3",
  };

  return (
    <div
      className={cn(
        spacingClasses[spacing],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

// FormGroup for grouping related form fields
const FormGroup = ({ 
  children, 
  className, 
  layout = "vertical",
  spacing = "default",
  ...props 
}) => {
  const layoutClasses = {
    vertical: "space-y-4",
    horizontal: "grid grid-cols-1 sm:grid-cols-2 gap-4",
    inline: "flex flex-wrap gap-4",
  };

  const spacingClasses = {
    tight: layout === "vertical" ? "space-y-3" : "gap-3",
    default: layout === "vertical" ? "space-y-4" : "gap-4", 
    loose: layout === "vertical" ? "space-y-6" : "gap-6",
  };

  return (
    <div
      className={cn(
        layout === "vertical" ? spacingClasses[spacing] : layoutClasses[layout],
        layout !== "vertical" && spacingClasses[spacing],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

// FormSection for grouping form sections with titles
const FormSection = ({ 
  title,
  description,
  children,
  className,
  ...props 
}) => {
  return (
    <div className={cn("space-y-4", className)} {...props}>
      {(title || description) && (
        <div className="space-y-1">
          {title && (
            <h3 className="text-base font-semibold text-gray-900 dark:text-gray-100">
              {title}
            </h3>
          )}
          {description && (
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {description}
            </p>
          )}
        </div>
      )}
      {children}
    </div>
  );
};

// FormError for consistent error message display
const FormError = ({ 
  children, 
  className,
  ...props 
}) => {
  if (!children) return null;

  return (
    <p
      className={cn(
        "text-sm text-red-600 dark:text-red-400",
        className
      )}
      role="alert"
      {...props}
    >
      {children}
    </p>
  );
};

// FormHelp for consistent help text display
const FormHelp = ({ 
  children, 
  className,
  ...props 
}) => {
  if (!children) return null;

  return (
    <p
      className={cn(
        "text-sm text-gray-500 dark:text-gray-400",
        className
      )}
      {...props}
    >
      {children}
    </p>
  );
};

// FormLabel wrapper for consistent label styling
const FormLabel = ({ 
  children, 
  required,
  className,
  ...props 
}) => {
  return (
    <Label
      required={required}
      className={cn("block", className)}
      {...props}
    >
      {children}
    </Label>
  );
};

export { 
  FormField, 
  FormGroup, 
  FormSection, 
  FormError, 
  FormHelp, 
  FormLabel 
};