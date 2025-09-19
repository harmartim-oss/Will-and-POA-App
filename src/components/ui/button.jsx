import * as React from "react"
import { cva } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  [
    "inline-flex items-center justify-center rounded-md text-sm font-medium",
    "transition-all duration-200 ease-out",
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2",
    "disabled:pointer-events-none disabled:opacity-50",
    "relative overflow-hidden",
  ],
  {
    variants: {
      variant: {
        primary: [
          "bg-blue-600 text-white shadow-sm",
          "hover:bg-blue-700 hover:shadow-md",
          "active:bg-blue-800",
          "focus-visible:ring-blue-500",
          "dark:bg-blue-500 dark:hover:bg-blue-400 dark:active:bg-blue-300",
        ],
        secondary: [
          "bg-gray-100 text-gray-900 border border-gray-200",
          "hover:bg-gray-200 hover:border-gray-300",
          "active:bg-gray-300",
          "focus-visible:ring-gray-500",
          "dark:bg-gray-700 dark:text-gray-100 dark:border-gray-600",
          "dark:hover:bg-gray-600 dark:hover:border-gray-500",
          "dark:active:bg-gray-500",
        ],
        subtle: [
          "bg-gray-50 text-gray-700 border border-gray-100",
          "hover:bg-gray-100 hover:border-gray-200",
          "active:bg-gray-200",
          "focus-visible:ring-gray-400",
          "dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700",
          "dark:hover:bg-gray-700 dark:hover:border-gray-600",
          "dark:active:bg-gray-600",
        ],
        outline: [
          "border border-gray-300 bg-transparent text-gray-700",
          "hover:bg-gray-50 hover:text-gray-900",
          "active:bg-gray-100",
          "focus-visible:ring-gray-500",
          "dark:border-gray-600 dark:text-gray-300",
          "dark:hover:bg-gray-700 dark:hover:text-gray-100",
          "dark:active:bg-gray-600",
        ],
        ghost: [
          "text-gray-700 bg-transparent",
          "hover:bg-gray-100 hover:text-gray-900",
          "active:bg-gray-200",
          "focus-visible:ring-gray-500",
          "dark:text-gray-300",
          "dark:hover:bg-gray-700 dark:hover:text-gray-100",
          "dark:active:bg-gray-600",
        ],
        danger: [
          "bg-red-600 text-white shadow-sm",
          "hover:bg-red-700 hover:shadow-md",
          "active:bg-red-800",
          "focus-visible:ring-red-500",
          "dark:bg-red-500 dark:hover:bg-red-400 dark:active:bg-red-300",
        ],
        link: [
          "text-blue-600 underline-offset-4 bg-transparent p-0 h-auto",
          "hover:underline hover:text-blue-700",
          "focus-visible:ring-blue-500",
          "dark:text-blue-400 dark:hover:text-blue-300",
        ],
      },
      size: {
        sm: "h-8 px-3 text-xs rounded-md",
        default: "h-10 px-4 py-2 rounded-md",
        lg: "h-12 px-6 text-base rounded-lg",
        xl: "h-14 px-8 text-lg rounded-lg",
        icon: "h-10 w-10 rounded-md",
        "icon-sm": "h-8 w-8 rounded-md",
        "icon-lg": "h-12 w-12 rounded-lg",
      },
      fullWidth: {
        true: "w-full",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "default",
    },
  }
)

const Button = React.forwardRef(({ 
  className, 
  variant, 
  size, 
  fullWidth,
  children,
  ...props 
}, ref) => {
  return (
    <button
      className={cn(buttonVariants({ variant, size, fullWidth, className }))}
      ref={ref}
      {...props}
    >
      {children}
    </button>
  )
})
Button.displayName = "Button"

export { Button, buttonVariants }