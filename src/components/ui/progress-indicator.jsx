import React from 'react';
import { motion } from 'framer-motion';
import { Check, Circle, ArrowRight } from 'lucide-react';
import { cn } from '../../lib/utils';

const ProgressIndicator = ({ 
  steps, 
  currentStep, 
  className,
  variant = "default",
  showLabels = true,
  orientation = "horizontal"
}) => {
  const isHorizontal = orientation === "horizontal";
  
  const getStepStatus = (stepIndex) => {
    if (stepIndex < currentStep) return 'completed';
    if (stepIndex === currentStep) return 'current';
    return 'upcoming';
  };

  const getStepIcon = (stepIndex, status) => {
    switch (status) {
      case 'completed':
        return <Check className="w-4 h-4" />;
      case 'current':
        return (
          <motion.div
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="w-2 h-2 bg-current rounded-full"
          />
        );
      default:
        return <Circle className="w-4 h-4" />;
    }
  };

  const getStepColors = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-600 text-white border-green-600';
      case 'current':
        return 'bg-blue-600 text-white border-blue-600';
      default:
        return 'bg-gray-200 text-gray-400 border-gray-200 dark:bg-gray-700 dark:text-gray-500 dark:border-gray-700';
    }
  };

  const getConnectorColors = (stepIndex) => {
    const isCompleted = stepIndex < currentStep;
    return isCompleted 
      ? 'bg-green-600' 
      : 'bg-gray-200 dark:bg-gray-700';
  };

  if (variant === "compact") {
    return (
      <div className={cn("flex items-center space-x-2", className)}>
        <div className="flex items-center space-x-1">
          {steps.map((_, index) => (
            <div
              key={index}
              className={cn(
                "w-2 h-2 rounded-full transition-colors duration-200",
                index <= currentStep 
                  ? "bg-blue-600" 
                  : "bg-gray-300 dark:bg-gray-600"
              )}
            />
          ))}
        </div>
        <span className="text-sm text-gray-600 dark:text-gray-400">
          {currentStep + 1} of {steps.length}
        </span>
      </div>
    );
  }

  return (
    <div className={cn(
      "flex",
      isHorizontal ? "items-center" : "flex-col space-y-4",
      className
    )}>
      {steps.map((step, index) => {
        const status = getStepStatus(index);
        const isLast = index === steps.length - 1;

        return (
          <div
            key={index}
            className={cn(
              "flex items-center",
              !isHorizontal && "w-full"
            )}
          >
            {/* Step circle */}
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: index * 0.1 }}
              className={cn(
                "relative flex items-center justify-center w-10 h-10 rounded-full border-2 transition-all duration-200",
                getStepColors(status)
              )}
            >
              {getStepIcon(index, status)}
              
              {/* Step number for upcoming steps */}
              {status === 'upcoming' && (
                <span className="text-sm font-medium">
                  {index + 1}
                </span>
              )}
            </motion.div>

            {/* Step label */}
            {showLabels && (
              <motion.div
                initial={{ opacity: 0, x: isHorizontal ? -10 : 0, y: isHorizontal ? 0 : -10 }}
                animate={{ opacity: 1, x: 0, y: 0 }}
                transition={{ delay: index * 0.1 + 0.1 }}
                className={cn(
                  isHorizontal ? "ml-3" : "mt-2 text-center",
                  "flex-1"
                )}
              >
                <div className={cn(
                  "font-medium transition-colors duration-200",
                  status === 'current' 
                    ? "text-blue-900 dark:text-blue-100" 
                    : status === 'completed'
                    ? "text-green-900 dark:text-green-100"
                    : "text-gray-500 dark:text-gray-400"
                )}>
                  {step.title}
                </div>
                {step.description && (
                  <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    {step.description}
                  </div>
                )}
              </motion.div>
            )}

            {/* Connector line */}
            {!isLast && (
              <motion.div
                initial={{ scaleX: 0 }}
                animate={{ scaleX: 1 }}
                transition={{ delay: index * 0.1 + 0.2, duration: 0.3 }}
                className={cn(
                  "transition-colors duration-200",
                  isHorizontal 
                    ? "h-0.5 flex-1 mx-4" 
                    : "w-0.5 h-8 ml-5",
                  getConnectorColors(index)
                )}
              />
            )}
          </div>
        );
      })}
    </div>
  );
};

// Progress bar variant
const ProgressBar = ({ 
  value, 
  max = 100, 
  className,
  showPercentage = true,
  label,
  color = "blue"
}) => {
  const percentage = Math.min((value / max) * 100, 100);
  
  const colorClasses = {
    blue: "bg-blue-600",
    green: "bg-green-600", 
    red: "bg-red-600",
    yellow: "bg-yellow-600"
  };

  return (
    <div className={cn("space-y-2", className)}>
      {(label || showPercentage) && (
        <div className="flex justify-between items-center text-sm">
          {label && (
            <span className="font-medium text-gray-700 dark:text-gray-300">
              {label}
            </span>
          )}
          {showPercentage && (
            <span className="text-gray-600 dark:text-gray-400">
              {Math.round(percentage)}%
            </span>
          )}
        </div>
      )}
      
      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className={cn(
            "h-full rounded-full transition-all duration-300",
            colorClasses[color]
          )}
        />
      </div>
    </div>
  );
};

export { ProgressIndicator, ProgressBar };
