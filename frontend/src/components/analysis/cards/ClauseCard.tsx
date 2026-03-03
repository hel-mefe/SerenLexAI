import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, AlertTriangle, Lightbulb } from 'lucide-react'

import type { SeverityLevel } from '@/types/analysis'

type Props = {
  title: string
  severity: SeverityLevel
  originalText: string
  riskExplanation: string
  recommendation: string
}

interface SeverityStyle {
  dot: string
  badge: string
  border: string
}

const SEVERITY_STYLES: Record<SeverityLevel, SeverityStyle> = {
  High: {
    dot: 'bg-red-500',
    badge: 'bg-red-100 text-red-600',
    border: 'border-l-red-500',
  },
  Medium: {
    dot: 'bg-amber-500',
    badge: 'bg-amber-100 text-amber-600',
    border: 'border-l-amber-500',
  },
  Low: {
    dot: 'bg-emerald-500',
    badge: 'bg-emerald-100 text-emerald-600',
    border: 'border-l-emerald-500',
  },
}

const FALLBACK_STYLE: SeverityStyle = {
  dot: 'bg-slate-400',
  badge: 'bg-slate-100 text-slate-600',
  border: 'border-l-slate-400',
}

export function ClauseCard({
  title,
  severity,
  originalText,
  riskExplanation,
  recommendation,
}: Props) {
  const [open, setOpen] = useState(true)

  const normalised = severity?.toLowerCase() as SeverityLevel | undefined
  const styles: SeverityStyle = (normalised && SEVERITY_STYLES[normalised]) ?? FALLBACK_STYLE

  return (
    <div
      className={`
        rounded-2xl overflow-hidden transition-all
        bg-white/90 backdrop-blur
        border border-black/5 border-l-4 ${styles.border}
      `}
    >
      {/* Header */}
      <button
        onClick={() => setOpen((prev) => !prev)}
        className="w-full flex items-center justify-between px-6 py-5 hover:bg-slate-50/60 transition-colors text-left"
      >
        <div className="flex items-center gap-4">
          <div className={`w-2.5 h-2.5 rounded-full ${styles.dot}`} />

          <span className={`px-2.5 py-1 rounded-lg text-xs font-bold ${styles.badge}`}>
            {severity}
          </span>

          <span className="text-sm font-bold text-slate-900">
            {title}
          </span>
        </div>

        <ChevronDown
          className={`w-5 h-5 text-slate-400 transition-transform ${open ? 'rotate-180' : ''}`}
        />
      </button>

      {/* Expandable Content */}
      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="px-6 pb-6 border-t border-slate-100 space-y-4 overflow-hidden"
          >
            {/* Original Clause */}
            <div className="mt-4 p-4 rounded-xl border-l-4 bg-slate-50 border-slate-300">
              <div className="text-xs font-bold text-slate-400 uppercase tracking-wide mb-2">
                Original Clause
              </div>
              <p className="text-sm text-slate-700 italic leading-relaxed">
                {originalText}
              </p>
            </div>

            {/* Why Risky */}
            <div className="p-4 rounded-xl bg-amber-50 border border-amber-100">
              <div className="flex items-center gap-2 mb-2">
                <AlertTriangle className="w-4 h-4 text-amber-500" />
                <span className="text-xs font-bold text-amber-700 uppercase tracking-wide">
                  Why This Is Risky
                </span>
              </div>
              <p className="text-sm text-slate-700 leading-relaxed">
                {riskExplanation}
              </p>
            </div>

            {/* Recommended Action */}
            <div className="p-4 rounded-xl border border-emerald-100 bg-gradient-to-br from-emerald-50/60 to-emerald-50/30">
              <div className="flex items-center gap-2 mb-2">
                <Lightbulb className="w-4 h-4 text-emerald-600" />
                <span className="text-xs font-bold text-emerald-700 uppercase tracking-wide">
                  Recommended Action
                </span>
              </div>
              <p className="text-sm text-slate-700 leading-relaxed">
                {recommendation}
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}