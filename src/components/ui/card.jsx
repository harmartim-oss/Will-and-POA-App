import * as React from "react"
import { cn } from "@/lib/utils"

const elevations = {
  none: "shadow-none",
  sm: "elevation-1",
  md: "elevation-2",
  lg: "elevation-3",
}

const Card = React.forwardRef(({ className, elevation = 'sm', interactive = false, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
  "rounded-lg border bg-[var(--surface-3)] text-[var(--text-strong)] border-[var(--border-subtle)] transition-shadow",
  elevations[elevation],
  interactive && "hover:elevation-2 active:elevation-1",
  interactive && "focus-ring-custom",
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