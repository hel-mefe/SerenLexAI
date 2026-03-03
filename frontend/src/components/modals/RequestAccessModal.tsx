import { motion, AnimatePresence } from 'framer-motion'
import { X, Copy, Check } from 'lucide-react'
import { ASSESSMENT_CREDENTIALS } from '@/config'
import { useState } from 'react'

type Props = {
  open: boolean
  onClose: () => void
}

type CopyField = 'username' | 'password' | null

export function RequestAccessModal({ open, onClose }: Props) {
  const [copiedField, setCopiedField] = useState<CopyField>(null)

  const handleCopy = async (
    value: string,
    field: Exclude<CopyField, null>
  ) => {
    try {
      await navigator.clipboard.writeText(value)
      setCopiedField(field)

      setTimeout(() => {
        setCopiedField(null)
      }, 1500)
    } catch (err) {
      console.error('Clipboard copy failed', err)
    }
  }

  return (
    <AnimatePresence>
      {open && (
        <>
          {/* Overlay */}
          <motion.div
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Modal */}
          <motion.div
            className="fixed inset-0 flex items-center justify-center z-50 p-6"
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.96 }}
            transition={{ duration: 0.2 }}
          >
            <div
              className="w-full max-w-md rounded-3xl bg-auth-gradient shadow-glow p-8 relative border border-white/10"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Close */}
              <button
                onClick={onClose}
                className="absolute top-4 right-4 text-white/40 hover:text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </button>

              <h3 className="text-xl font-bold text-white mb-4">
                Assessment Access Credentials
              </h3>

              <p className="text-sm text-white/50 mb-6">
                Use the following credentials to explore the platform.
              </p>

              <div className="bg-white/5 rounded-2xl p-5 space-y-5 border border-white/10">
                {/* Username */}
                <div className="flex items-center justify-between">
                  <div>
                    <span className="block text-xs uppercase text-white/40 mb-1">
                      Username
                    </span>
                    <span className="text-sm font-semibold text-white">
                      {ASSESSMENT_CREDENTIALS.username}
                    </span>
                  </div>

                  <button
                    onClick={() =>
                      handleCopy(
                        ASSESSMENT_CREDENTIALS.username,
                        'username'
                      )
                    }
                    className="text-white/40 hover:text-white transition-colors"
                  >
                    {copiedField === 'username' ? (
                      <Check className="w-4 h-4 text-emerald-400" />
                    ) : (
                      <Copy className="w-4 h-4" />
                    )}
                  </button>
                </div>

                {/* Password */}
                <div className="flex items-center justify-between">
                  <div>
                    <span className="block text-xs uppercase text-white/40 mb-1">
                      Password
                    </span>
                    <span className="text-sm font-semibold text-white">
                      {ASSESSMENT_CREDENTIALS.password}
                    </span>
                  </div>

                  <button
                    onClick={() =>
                      handleCopy(
                        ASSESSMENT_CREDENTIALS.password,
                        'password'
                      )
                    }
                    className="text-white/40 hover:text-white transition-colors"
                  >
                    {copiedField === 'password' ? (
                      <Check className="w-4 h-4 text-emerald-400" />
                    ) : (
                      <Copy className="w-4 h-4" />
                    )}
                  </button>
                </div>
              </div>

              <p className="text-xs text-white/40 mt-6">
                These credentials are provided for evaluation
                purposes only.
              </p>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}