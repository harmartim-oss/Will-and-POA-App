import React from 'react';
import { cn } from '@/lib/utils';
import { Check, Circle, Minus } from 'lucide-react';

const Stepper = ({ 
  steps, 
  currentStep = 0, 
  variant = "default",
  orientation = "horizontal",
  className,
  onStepClick,
  ...props 
}) => {
  const isHorizontal = orientation === "horizontal";
  const isVertical = orientation === "vertical";

  return (
    <div
      className={cn(
        "flex",
        isHorizontal && "items-center justify-between w-full",
        isVertical && "flex-col space-y-4",
        className
      )}
      role="navigation"
      aria-label="Progress steps"
      {...props}
    >
      {steps.map((step, index) => {
        const isActive = index === currentStep;
        const isCompleted = index < currentStep;
        const isUpcoming = index > currentStep;
        const isClickable = onStepClick && (isCompleted || isActive);
        const isLast = index === steps.length - 1;

        return (
          <React.Fragment key={step.id || index}>
            <StepItem
              step={step}
              index={index}
              isActive={isActive}
              isCompleted={isCompleted}
              isUpcoming={isUpcoming}
              isClickable={isClickable}
              variant={variant}
              orientation={orientation}
              onClick={isClickable ? () => onStepClick(index) : undefined}
            />
            
            {!isLast && (
              <StepConnector
                isCompleted={isCompleted}
                orientation={orientation}
                variant={variant}
              />
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
};

const StepItem = ({
  step,
  index,
  isActive,
  isCompleted,
  isUpcoming,
  isClickable,
  variant,
  orientation,
  onClick
}) => {
  const isHorizontal = orientation === "horizontal";
  const isVertical = orientation === "vertical";

  const handleClick = () => {
    if (onClick) onClick();
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      if (onClick) onClick();
    }
  };

  return (
    <div
      className={cn(
        "flex items-center",
        isHorizontal && "flex-col text-center",
        isVertical && "flex-row space-x-3",
        isClickable && "cursor-pointer group",
        "focus-within:outline-none"
      )}
      onClick={isClickable ? handleClick : undefined}
    >
      {/* Step indicator */}
      <div
        className={cn(
          "relative flex items-center justify-center rounded-full border-2 transition-all duration-200",
          "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
          isClickable && "focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2",
          // Size variations
          variant === "compact" ? "h-6 w-6 text-xs" : "h-8 w-8 text-sm",
          // State-based styling
          isActive && [
            "border-blue-600 bg-blue-600 text-white",
            "dark:border-blue-500 dark:bg-blue-500",
            isClickable && "group-hover:border-blue-700 group-hover:bg-blue-700"
          ],
          isCompleted && [
            "border-green-600 bg-green-600 text-white", 
            "dark:border-green-500 dark:bg-green-500",
            isClickable && "group-hover:border-green-700 group-hover:bg-green-700"
          ],
          isUpcoming && [
            "border-gray-300 bg-white text-gray-500",
            "dark:border-gray-600 dark:bg-gray-800 dark:text-gray-400"
          ]
        )}
        tabIndex={isClickable ? 0 : -1}
        onKeyDown={isClickable ? handleKeyDown : undefined}
        role={isClickable ? "button" : undefined}
        aria-label={isClickable ? `Go to step ${index + 1}: ${step.title}` : undefined}
      >
        {isCompleted ? (
          <Check className="h-4 w-4" />
        ) : isActive ? (
          <Circle className="h-3 w-3 fill-current" />
        ) : (
          <span className="font-medium">{index + 1}</span>
        )}
      </div>

      {/* Step content */}
      <div
        className={cn(
          "flex flex-col",
          isHorizontal && "mt-2 max-w-[120px]",
          isVertical && "flex-1 min-w-0"
        )}
      >
        <div
          className={cn(
            "font-medium transition-colors duration-200",
            variant === "compact" ? "text-xs" : "text-sm",
            isActive && "text-blue-700 dark:text-blue-400",
            isCompleted && "text-green-700 dark:text-green-400", 
            isUpcoming && "text-gray-500 dark:text-gray-400",
            isClickable && isActive && "group-hover:text-blue-800 dark:group-hover:text-blue-300",
            isClickable && isCompleted && "group-hover:text-green-800 dark:group-hover:text-green-300"
          )}
        >
          {step.title}
        </div>
        
        {step.description && variant !== "compact" && (
          <div
            className={cn(
              "text-xs text-gray-500 dark:text-gray-400 mt-0.5",
              isHorizontal && "line-clamp-2",
              isVertical && "line-clamp-1"
            )}
          >
            {step.description}
          </div>
        )}
      </div>
    </div>
  );
};

const StepConnector = ({ isCompleted, orientation, variant }) => {
  const isHorizontal = orientation === "horizontal";
  
  return (
    <div
      className={cn(
        "transition-colors duration-200",
        isHorizontal && [
          "flex-1 h-0.5 mx-2",
          variant === "compact" && "mx-1"
        ],
        orientation === "vertical" && "h-8 w-0.5 ml-3",
        isCompleted 
          ? "bg-green-600 dark:bg-green-500" 
          : "bg-gray-300 dark:bg-gray-600"
      )}
      aria-hidden="true"
    />
  );
};

// Preset configurations for common use cases
Stepper.Wizard = ({ steps, currentStep, onStepClick, ...props }) => (
  <Stepper
    steps={steps}
    currentStep={currentStep}
    onStepClick={onStepClick}
    variant="default"
    orientation="horizontal"
    {...props}
  />
);

Stepper.Progress = ({ steps, currentStep, ...props }) => (
  <Stepper
    steps={steps}
    currentStep={currentStep}
    variant="compact"
    orientation="horizontal"
    {...props}
  />
);

Stepper.Sidebar = ({ steps, currentStep, onStepClick, ...props }) => (
  <Stepper
    steps={steps}
    currentStep={currentStep}
    onStepClick={onStepClick}
    variant="default"
    orientation="vertical"
    {...props}
  />
);

export { Stepper };