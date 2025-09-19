import * as React from "react"
import { cn } from "@/lib/utils"

// Variant styles leverage semantic design tokens via utility classes referencing CSS vars
const buttonVariants = {
  primary: "bg-[var(--btn-primary-bg)] text-[var(--btn-primary-text)] hover:bg-[var(--btn-primary-bg-hover)] active:bg-[var(--btn-primary-bg-active)] focus-visible:ring-[var(--btn-primary-ring)] shadow-lg hover:shadow-xl transition-all duration-200",
  secondary: "bg-[var(--btn-secondary-bg)] text-[var(--btn-secondary-text)] hover:bg-[var(--btn-secondary-bg-hover)] active:bg-[var(--btn-secondary-bg-active)] shadow-md hover:shadow-lg transition-all duration-200",
  outline: "border border-[var(--border-default)] text-[var(--text-strong)] bg-transparent hover:bg-[var(--surface-alt)] hover:border-[var(--color-primary-500)] transition-all duration-200",
  subtle: "bg-[var(--surface-muted)] text-[var(--text-strong)] hover:bg-[var(--surface-alt)] hover:shadow-md transition-all duration-200",
  ghost: "bg-transparent hover:bg-[var(--surface-muted)] transition-all duration-200",
  destructive: "bg-red-600 text-white hover:bg-red-700 active:bg-red-800 shadow-md hover:shadow-lg transition-all duration-200",
  link: "text-[var(--text-accent)] underline-offset-4 hover:underline bg-transparent p-0 h-auto transition-colors duration-200",
}

const buttonSizes = {
  default: "h-10 px-4 py-2",
  sm: "h-9 px-3 text-sm",
  lg: "h-12 px-6 text-base",
  xl: "h-14 px-8 text-lg",
  icon: "h-10 w-10 p-0",
}

const Button = React.forwardRef(({ className, variant = "primary", size = "default", loading = false, disabled, children, asChild, ...props }, ref) => {
  const Comp = asChild ? 'span' : 'button'
  return (
    <Comp
      className={cn(
  "relative inline-flex items-center justify-center gap-2 rounded-md font-medium select-none whitespace-nowrap disabled:pointer-events-none disabled:opacity-50 overflow-hidden transform-gpu",
  "focus-ring-custom ring-offset-[var(--surface-1)]",
  "transition-[background,color,box-shadow,transform,border-color] active:scale-[.98] will-change-transform",
  "duration-[var(--motion-fast)] ease-standard hover:translate-y-[-1px]",
        buttonVariants[variant],
        buttonSizes[size],
        loading && "cursor-progress",
        className
      )}
      ref={ref}
      disabled={disabled || loading}
      aria-busy={loading || undefined}
      aria-live={loading ? 'polite' : undefined}
      {...props}
    >
      {loading && (
        <span className="absolute inset-0 flex items-center justify-center" aria-hidden="true">
          <span className="h-5 w-5 animate-spin rounded-full border-2 border-[var(--btn-primary-text)] border-t-transparent" />
        </span>
      )}
      <span className={cn(loading && "opacity-0")}>{children}</span>
    </Comp>
  )
})
Button.displayName = "Button"

export { Button, buttonVariants }