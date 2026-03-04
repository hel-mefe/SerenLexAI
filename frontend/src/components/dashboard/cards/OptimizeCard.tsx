import { motion } from 'framer-motion'
import { Sparkles } from 'lucide-react'

export function OptimizeCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.5 }}
      className="rounded-2xl p-6 relative overflow-hidden text-white
      bg-gradient-to-br from-[#1a1f2e] to-[#2d3550] shadow-xl"
    >
      <div className="relative z-10">
        <div className="flex items-center gap-2 mb-3">
          <Sparkles className="w-4 h-4 text-amber-400" />
          <span className="text-xs font-semibold text-amber-400 uppercase">
            Quick note
          </span>
        </div>

        <p className="text-sm opacity-80">
          SerenLexAI groups similar clauses, surfaces hidden obligations, and
          explains legal language in plain English so non‑lawyers can review
          complex contracts with confidence.
        </p>
      </div>
    </motion.div>
  )
}