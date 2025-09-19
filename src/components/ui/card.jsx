import * as React from "react"
import { cn } from "@/lib/utils"

const elevations = {
  none: "shadow-none",
  sm: "shadow-sm",
  md: "shadow-md",
  lg: "shadow-lg",
}

const Card = React.forwardRef(({ className, elevation = 'sm', interactive = false, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-lg border bg-[var(--surface-elevated)] text-[var(--text-strong)] border-[var(--border-subtle)] transition-shadow",
      elevations[elevation],
      interactive && "hover:shadow-md active:shadow-sm",
      interactive && "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 ring-offset-[var(--surface-bg)] focus-visible:ring-[var(--btn-primary-bg)]",
      className
    )}
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
    className={cn("text-sm text-gray-500", className)}
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