import * as React from "react"
import { cn } from "@/lib/utils"

const Card = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      [
        "rounded-lg border bg-white text-gray-950 shadow-sm",
        "border-gray-200 dark:border-gray-700",
        "dark:bg-gray-800 dark:text-gray-50",
        "transition-colors duration-200",
      ],
      className
    )}
    {...props}
  />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-2 p-6 pb-4", className)}
    {...props}
  />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef(({ className, level = 3, ...props }, ref) => {
  const Component = `h${level}`;
  
  const sizeClasses = {
    1: "text-3xl font-bold leading-tight tracking-tight",
    2: "text-2xl font-bold leading-tight tracking-tight", 
    3: "text-xl font-semibold leading-none tracking-tight",
    4: "text-lg font-semibold leading-none tracking-tight",
    5: "text-base font-semibold leading-none tracking-tight",
    6: "text-sm font-semibold leading-none tracking-tight",
  };

  return (
    <Component
      ref={ref}
      className={cn(
        sizeClasses[level] || sizeClasses[3],
        "text-gray-900 dark:text-gray-50",
        className
      )}
      {...props}
    />
  )
})
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn(
      "text-sm leading-relaxed text-gray-600 dark:text-gray-400",
      className
    )}
    {...props}
  />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef(({ className, ...props }, ref) => (
  <div 
    ref={ref} 
    className={cn("p-6 pt-0", className)} 
    {...props} 
  />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "flex items-center justify-between p-6 pt-0",
      className
    )}
    {...props}
  />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }