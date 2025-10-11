import React from 'react';
import { Check } from 'lucide-react';

export const Checkbox = ({ checked, onCheckedChange, id, className = '' }) => {
  return (
    <button
      type="button"
      role="checkbox"
      aria-checked={checked}
      onClick={() => onCheckedChange?.(!checked)}
      id={id}
      className={`peer h-5 w-5 shrink-0 rounded border border-gray-300 dark:border-gray-600 ring-offset-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${
        checked ? 'bg-blue-600 border-blue-600 text-white' : 'bg-white dark:bg-gray-800'
      } ${className}`}
    >
      {checked && <Check className="h-4 w-4" />}
    </button>
  );
};
