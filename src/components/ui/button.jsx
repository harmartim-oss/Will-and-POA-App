import * as React from "react"
import { cn } from "@/lib/utils"

// Variant styles leverage semantic design tokens via utility classes referencing CSS vars
const buttonVariants = {
  primary: "bg-[var(--btn-primary-bg)] text-[var(--btn-primary-text)] hover:bg-[var(--btn-primary-bg-hover)] active:bg-[var(--btn-primary-bg-active)] focus-visible:ring-[var(--btn-primary-ring)]",
  secondary: "bg-[var(--btn-secondary-bg)] text-[var(--btn-secondary-text)] hover:bg-[var(--btn-secondary-bg-hover)] active:bg-[var(--btn-secondary-bg-active)]",
  outline: "border border-[var(--border-default)] text-[var(--text-strong)] bg-transparent hover:bg-[var(--surface-alt)]",
  subtle: "bg-[var(--surface-muted)] text-[var(--text-strong)] hover:bg-[var(--surface-alt)]",
  ghost: "bg-transparent hover:bg-[var(--surface-muted)]",
  destructive: "bg-red-600 text-white hover:bg-red-700 active:bg-red-800",
  link: "text-[var(--text-accent)] underline-offset-4 hover:underline bg-transparent p-0 h-auto",
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
        "relative inline-flex items-center justify-center gap-2 rounded-md font-medium transition-colors select-none whitespace-nowrap disabled:pointer-events-none disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 ring-offset-[var(--surface-bg)] shadow-sm active:scale-[.985]",
        "transition-[background,color,box-shadow,transform] duration-[var(--duration-fast)] ease-out",
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