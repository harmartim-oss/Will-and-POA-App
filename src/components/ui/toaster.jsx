import { useToast } from '@/hooks/use-toast'
import { X } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const Toaster = () => {
  const { toasts, dismiss } = useToast()

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      <AnimatePresence>
        {toasts.map((toast) => (
          <motion.div
            key={toast.id}
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 100 }}
            className={`
              max-w-sm p-4 rounded-lg shadow-lg border
              ${toast.variant === 'destructive' 
                ? 'bg-red-50 border-red-200 text-red-900' 
                : 'bg-white border-gray-200 text-gray-900'
              }
            `}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                {toast.title && (
                  <div className="font-medium text-sm">{toast.title}</div>
                )}
                {toast.description && (
                  <div className="text-sm opacity-90 mt-1">{toast.description}</div>
                )}
              </div>
              <button
                onClick={() => dismiss(toast.id)}
                className="ml-2 opacity-50 hover:opacity-100"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  )
}

export { Toaster }

