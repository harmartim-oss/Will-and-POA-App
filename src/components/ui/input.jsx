import * as React from "react"
import { cn } from "@/lib/utils"

const sizes = {
  sm: "h-9 text-sm px-3",
  md: "h-10 text-sm px-3",
  lg: "h-12 text-base px-4",
}

const Input = React.forwardRef(({ className, type = 'text', size = 'md', invalid = false, loading = false, ...props }, ref) => {
  return (
    <div className={cn("relative", loading && "opacity-80")}> 
      <input
        type={type}
        data-invalid={invalid || undefined}
        className={cn(
          "flex w-full rounded-xl border-2 bg-white/80 backdrop-blur-sm text-gray-900 placeholder:text-gray-500",
          "border-gray-200 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-[var(--color-brand-300)] focus-visible:ring-offset-2 focus-visible:border-[var(--color-brand-500)]",
          "hover:border-[var(--color-brand-300)] hover:shadow-sm hover:bg-white",
          "disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-300 ease-out",
          sizes[size],
          "file:border-0 file:bg-transparent file:text-sm file:font-medium",
          "data-[invalid=true]:border-red-300 data-[invalid=true]:bg-red-50 data-[invalid=true]:focus-visible:ring-red-300 data-[invalid=true]:focus-visible:border-red-500",
          className
        )}
        aria-invalid={invalid || undefined}
        ref={ref}
        {...props}
      />
      {loading && (
        <span className="pointer-events-none absolute inset-y-0 right-3 flex items-center" aria-hidden="true">
          <span className="h-4 w-4 animate-spin rounded-full border-2 border-[var(--color-brand-600)] border-t-transparent" />
        </span>
      )}
    </div>
  )
})
Input.displayName = "Input"

export { Input }