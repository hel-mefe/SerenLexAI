import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, AlertTriangle, Lightbulb } from 'lucide-react'

import type { SeverityLevel } from '@/types/analysis'
import { getClauseTypeDisplayLabel } from '@/lib/clauseTypeLabels'

type Props = {
  title: string
  clauseType?: string | null
  severity: SeverityLevel
  originalText: string
  riskExplanation: string
  recommendation: string
}

/** Only the severity label (High/Medium/Low) is colored; the rest of the row is neutral */
interface SeverityStyle {
  badge: string
}

const SEVERITY_STYLES: Record<SeverityLevel, SeverityStyle> = {
  High: { badge: 'bg-risk-high-bg text-risk-high' },
  Medium: { badge: 'bg-risk-medium-bg text-risk-medium' },
  Low: { badge: 'bg-risk-low-bg text-risk-low' },
}

const FALLBACK_STYLE: SeverityStyle = {
  badge: 'bg-slate-100 text-slate-600',
}

export function ClauseCard({
  title,
  clauseType,
  severity,
  originalText,
  riskExplanation,
  recommendation,
}: Props) {
  const [open, setOpen] = useState(true)
  const displayTitle = getClauseTypeDisplayLabel(clauseType, title)

  const normalised: SeverityLevel | undefined = severity
    ? (severity.charAt(0).toUpperCase() + severity.slice(1).toLowerCase()) as SeverityLevel
    : undefined
  const styles: SeverityStyle = (normalised && SEVERITY_STYLES[normalised]) ?? FALLBACK_STYLE

  return (
    <div className="rounded-2xl overflow-hidden transition-all border border-slate-200 bg-surface-card">
      <button
        onClick={() => setOpen((prev) => !prev)}
        className="w-full flex items-center justify-between px-6 py-5 transition-colors text-left bg-surface-card hover:bg-slate-50/80 border-b border-slate-100"
      >
        <div className="flex items-center gap-4">
          <span className={`px-2.5 py-1 rounded-lg text-xs font-bold ${styles.badge}`}>
            {severity}
          </span>

          <span className="text-sm font-bold text-slate-900">
            {displayTitle}
          </span>
        </div>

        <ChevronDown
          className={`w-5 h-5 shrink-0 transition-transform text-slate-500 ${open ? 'rotate-180' : ''}`}
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
            className="px-6 pb-6 border-t border-slate-200/60 bg-white/95 space-y-4 overflow-hidden"
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
            <div className="p-4 rounded-xl border border-slate-200 bg-slate-50">
              <div className="flex items-center gap-2 mb-2 text-slate-600">
                <AlertTriangle className="w-4 h-4 shrink-0" />
                <span className="text-xs font-bold uppercase tracking-wide">
                  Why This Is Risky
                </span>
              </div>
              <p className="text-sm text-slate-700 leading-relaxed">
                {riskExplanation}
              </p>
            </div>

            {/* Recommended Action */}
            <div className="p-4 rounded-xl border border-risk-low bg-risk-low-bg">
              <div className="flex items-center gap-2 mb-2 text-risk-low">
                <Lightbulb className="w-4 h-4 shrink-0" />
                <span className="text-xs font-bold uppercase tracking-wide">
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