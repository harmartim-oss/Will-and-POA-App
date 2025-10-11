import React from 'react';
import { motion } from 'framer-motion';
import { Loader2, FileText, Brain, Shield } from 'lucide-react';

const EnhancedLoading = ({ 
  message = "Loading...", 
  submessage = "", 
  type = "default",
  size = "default" 
}) => {
  const sizeClasses = {
    small: "w-6 h-6",
    default: "w-8 h-8", 
    large: "w-12 h-12"
  };

  const containerClasses = {
    small: "p-4",
    default: "p-8",
    large: "p-12"
  };

  const getIcon = () => {
    switch (type) {
      case 'document':
        return FileText;
      case 'ai':
        return Brain;
      case 'legal':
        return Shield;
      default:
        return Loader2;
    }
  };

  const Icon = getIcon();

  return (
    <div className={`flex flex-col items-center justify-center ${containerClasses[size]}`}>
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
        className="mb-4"
      >
        <Icon className={`${sizeClasses[size]} text-blue-600 dark:text-blue-400`} />
      </motion.div>
      
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="text-center"
      >
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
          {message}
        </h3>
        {submessage && (
          <p className="text-sm text-gray-600 dark:text-gray-400">
            {submessage}
          </p>
        )}
      </motion.div>

      {/* Progress dots */}
      <motion.div 
        className="flex space-x-1 mt-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
      >
        {[0, 1, 2].map((i) => (
          <motion.div
            key={i}
            className="w-2 h-2 bg-blue-600 dark:bg-blue-400 rounded-full"
            animate={{ 
              scale: [1, 1.2, 1],
              opacity: [0.5, 1, 0.5]
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              delay: i * 0.2
            }}
          />
        ))}
      </motion.div>
    </div>
  );
};

export default EnhancedLoading;
