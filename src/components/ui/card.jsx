import * as React from "react"
import { cn } from "@/lib/utils"

const elevations = {
  none: "shadow-none",
  sm: "shadow-sm hover:shadow-md",
  md: "shadow-md hover:shadow-lg",
  lg: "shadow-lg hover:shadow-xl",
  xl: "shadow-xl hover:shadow-2xl",
}

const Card = React.forwardRef(({ className, elevation = 'sm', interactive = false, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-2xl border bg-white/80 backdrop-blur-sm text-gray-900 border-gray-200/60 transition-all duration-300",
      elevations[elevation],
      interactive && "hover:border-[var(--color-brand-300)] hover:-translate-y-1 cursor-pointer",
      interactive && "focus:outline-none focus-visible:ring-4 focus-visible:ring-[var(--color-brand-300)] focus-visible:ring-offset-2",
      className
    )}
    tabIndex={interactive ? 0 : undefined}
    {...props}
  />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-2xl font-semibold leading-none tracking-tight",
      className
    )}
    {...props}
  />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-gray-600 leading-relaxed", className)}
    {...props}
  />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props}
  />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }