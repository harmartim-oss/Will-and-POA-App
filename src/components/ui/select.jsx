import React from 'react';

export const Select = ({ children, value, onValueChange }) => {
  return (
    <div className="relative">
      {React.Children.map(children, child => {
        if (React.isValidElement(child)) {
          return React.cloneElement(child, { value, onValueChange });
        }
        return child;
      })}
    </div>
  );
};

export const SelectTrigger = ({ children, value, onValueChange }) => {
  const [isOpen, setIsOpen] = React.useState(false);
  
  return (
    <button
      type="button"
      onClick={() => setIsOpen(!isOpen)}
      className="flex h-10 w-full items-center justify-between rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-3 py-2 text-sm ring-offset-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {children}
    </button>
  );
};

export const SelectValue = ({ placeholder }) => {
  return <span className="text-gray-500 dark:text-gray-400">{placeholder}</span>;
};

export const SelectContent = ({ children }) => {
  return (
    <div className="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 shadow-lg">
      {children}
    </div>
  );
};

export const SelectItem = ({ value, children, onValueChange }) => {
  return (
    <button
      type="button"
      onClick={() => onValueChange?.(value)}
      className="relative flex w-full cursor-pointer select-none items-center rounded-sm py-2 px-3 text-sm outline-none hover:bg-blue-50 dark:hover:bg-blue-900/20 focus:bg-blue-50 dark:focus:bg-blue-900/20 text-gray-900 dark:text-gray-100"
    >
      {children}
    </button>
  );
};
