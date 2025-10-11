import React from 'react';

export const Alert = ({ children, variant = 'default', className = '' }) => {
  const variantClasses = {
    default: 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800 text-blue-900 dark:text-blue-100',
    destructive: 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800 text-red-900 dark:text-red-100',
    warning: 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800 text-yellow-900 dark:text-yellow-100',
    success: 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800 text-green-900 dark:text-green-100',
  };

  return (
    <div
      role="alert"
      className={`relative w-full rounded-lg border p-4 ${variantClasses[variant]} ${className}`}
    >
      {children}
    </div>
  );
};

export const AlertTitle = ({ children, className = '' }) => {
  return (
    <h5 className={`mb-1 font-medium leading-none tracking-tight ${className}`}>
      {children}
    </h5>
  );
};

export const AlertDescription = ({ children, className = '' }) => {
  return (
    <div className={`text-sm opacity-90 ${className}`}>
      {children}
    </div>
  );
};
