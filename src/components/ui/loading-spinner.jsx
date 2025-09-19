import { motion } from 'framer-motion'

const LoadingSpinner = ({ size = 'md', className = '', variant = 'primary' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16'
  }

  const variantClasses = {
    primary: 'border-[var(--color-brand-200)] border-t-[var(--color-brand-600)]',
    white: 'border-white/30 border-t-white',
    accent: 'border-[var(--color-accent-200)] border-t-[var(--color-accent-600)]'
  }

  return (
    <div className={`flex items-center justify-center ${className}`} role="status" aria-label="Loading">
      <motion.div
        className={`border-2 rounded-full ${sizeClasses[size]} ${variantClasses[variant]}`}
        animate={{ rotate: 360 }}
        transition={{
          duration: 1,
          repeat: Infinity,
          ease: "linear"
        }}
      />
      <span className="sr-only">Loading...</span>
    </div>
  )
}

export default LoadingSpinner