import * as React from "react"
import { cn } from "@/lib/utils"

// Enhanced variant styles with improved visual appeal and accessibility
const buttonVariants = {
  primary: "bg-gradient-to-r from-[var(--color-brand-600)] to-[var(--color-brand-500)] text-white hover:from-[var(--color-brand-700)] hover:to-[var(--color-brand-600)] active:from-[var(--color-brand-800)] active:to-[var(--color-brand-700)] focus-visible:ring-4 focus-visible:ring-[var(--color-brand-300)] shadow-lg hover:shadow-xl hover:shadow-[var(--color-brand-500)]/25 transition-all duration-300 transform hover:scale-[1.02]",
  secondary: "bg-white text-[var(--color-brand-700)] border-2 border-[var(--color-brand-200)] hover:bg-[var(--color-brand-50)] hover:border-[var(--color-brand-300)] active:bg-[var(--color-brand-100)] shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-[1.02]",
  outline: "border-2 border-[var(--color-brand-300)] text-[var(--color-brand-700)] bg-transparent hover:bg-[var(--color-brand-50)] hover:border-[var(--color-brand-400)] active:bg-[var(--color-brand-100)] transition-all duration-300 transform hover:scale-[1.02]",
  subtle: "bg-[var(--color-brand-50)] text-[var(--color-brand-700)] hover:bg-[var(--color-brand-100)] hover:shadow-md active:bg-[var(--color-brand-200)] transition-all duration-300",
  ghost: "bg-transparent hover:bg-[var(--color-brand-50)] text-[var(--color-brand-700)] transition-all duration-300",
  destructive: "bg-gradient-to-r from-red-600 to-red-500 text-white hover:from-red-700 hover:to-red-600 active:from-red-800 active:to-red-700 focus-visible:ring-4 focus-visible:ring-red-300 shadow-lg hover:shadow-xl hover:shadow-red-500/25 transition-all duration-300 transform hover:scale-[1.02]",
  link: "text-[var(--color-brand-600)] underline-offset-4 hover:underline hover:text-[var(--color-brand-700)] bg-transparent p-0 h-auto transition-colors duration-300",
}

const buttonSizes = {
  default: "h-11 px-6 py-2.5 text-sm font-medium",
  sm: "h-9 px-4 py-2 text-sm font-medium",
  lg: "h-12 px-8 py-3 text-base font-medium",
  xl: "h-14 px-10 py-4 text-lg font-semibold",
  icon: "h-11 w-11 p-0",
}

const Button = React.forwardRef(({ className, variant = "primary", size = "default", loading = false, disabled, children, asChild, ...props }, ref) => {
  const Comp = asChild ? 'span' : 'button'
  return (
    <Comp
      className={cn(
        "relative inline-flex items-center justify-center gap-2 rounded-xl font-medium select-none whitespace-nowrap disabled:pointer-events-none disabled:opacity-50 overflow-hidden transform-gpu",
        "focus:outline-none focus-visible:ring-4 focus-visible:ring-offset-2 focus-visible:ring-offset-white",
        "transition-[all] duration-[var(--motion-base)] ease-[var(--ease-standard)] will-change-transform",
        "disabled:transform-none disabled:shadow-none",
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