import * as React from "react"
import { cn } from "@/lib/utils"

const badgeVariants = {
  default: "border-transparent bg-gray-900 text-gray-50 hover:bg-gray-800 shadow-sm",
  secondary: "border-transparent bg-gray-100 text-gray-900 hover:bg-gray-200",
  success: "border-transparent bg-green-100 text-green-800 hover:bg-green-200",
  warning: "border-transparent bg-yellow-100 text-yellow-800 hover:bg-yellow-200", 
  danger: "border-transparent bg-red-100 text-red-800 hover:bg-red-200",
  info: "border-transparent bg-blue-100 text-blue-800 hover:bg-blue-200",
  brand: "border-transparent bg-gradient-to-r from-[var(--color-brand-500)] to-[var(--color-brand-400)] text-white shadow-sm",
  outline: "text-gray-950 border-gray-300 hover:bg-gray-50",
}

function Badge({ className, variant = "default", ...props }) {
  return (
    <div
      className={cn(
        "inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gray-950 focus:ring-offset-2",
        badgeVariants[variant],
        className
      )}
      {...props}
    />
  )
}

export { Badge, badgeVariants }