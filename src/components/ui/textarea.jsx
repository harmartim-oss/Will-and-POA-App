import * as React from "react"
import { cn } from "@/lib/utils"

const Textarea = React.forwardRef(({ className, invalid = false, ...props }, ref) => {
  return (
    <textarea
      className={cn(
        "flex min-h-[80px] w-full rounded-md border bg-[var(--input-bg)] text-[var(--input-text)] placeholder:text-[var(--input-placeholder)]",
        "border-[var(--input-border)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[var(--btn-primary-bg)] ring-offset-[var(--surface-bg)]",
        "hover:border-[var(--color-primary-400)] hover:shadow-sm px-3 py-2 text-sm",
        "disabled:cursor-not-allowed disabled:opacity-50 transition-[background,border,color,box-shadow] duration-200 ease-out",
        "resize-y",
        invalid && "border-[var(--status-danger-border)] bg-[var(--status-danger-bg)] focus-visible:ring-[var(--status-danger-border)]",
        className
      )}
      data-invalid={invalid || undefined}
      aria-invalid={invalid || undefined}
      ref={ref}
      {...props}
    />
  )
})
Textarea.displayName = "Textarea"

export { Textarea }