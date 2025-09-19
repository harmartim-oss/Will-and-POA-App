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
          "flex w-full rounded-md border bg-[var(--input-bg)] text-[var(--input-text)] placeholder:text-[var(--input-placeholder)]",
          "border-[var(--input-border)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[var(--btn-primary-bg)] ring-offset-[var(--surface-bg)]",
          "disabled:cursor-not-allowed disabled:opacity-50 transition-[background,border,color,box-shadow] duration-[var(--duration-fast)] ease-out",
          sizes[size],
          "file:border-0 file:bg-transparent file:text-sm file:font-medium",
          "data-[invalid=true]:border-[var(--status-danger-border)] data-[invalid=true]:bg-[var(--status-danger-bg)] data-[invalid=true]:focus-visible:ring-[var(--status-danger-border)]",
          className
        )}
        aria-invalid={invalid || undefined}
        ref={ref}
        {...props}
      />
      {loading && (
        <span className="pointer-events-none absolute inset-y-0 right-3 flex items-center" aria-hidden="true">
          <span className="h-4 w-4 animate-spin rounded-full border-2 border-[var(--btn-primary-bg)] border-t-transparent" />
        </span>
      )}
    </div>
  )
})
Input.displayName = "Input"

export { Input }