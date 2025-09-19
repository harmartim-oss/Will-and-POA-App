import * as React from "react"
import { cn } from "@/lib/utils"

const Input = React.forwardRef(({ className, type, ...props }, ref) => {
  return (
    <input
      type={type}
      className={cn(
        [
          "flex h-10 w-full rounded-md border bg-white px-3 py-2 text-sm",
          "border-gray-200 dark:border-gray-700",
          "dark:bg-gray-800 dark:text-gray-100",
          "placeholder:text-gray-500 dark:placeholder:text-gray-400",
          "ring-offset-white dark:ring-offset-gray-900",
          "file:border-0 file:bg-transparent file:text-sm file:font-medium",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2",
          "dark:focus-visible:ring-blue-400",
          "disabled:cursor-not-allowed disabled:opacity-50",
          "transition-colors duration-200",
        ],
        className
      )}
      ref={ref}
      {...props}
    />
  )
})
Input.displayName = "Input"

export { Input }