import { motion } from 'framer-motion'
import { useState } from 'react'
import { SeverityFilters } from '@/components/analysis/overview/SeverityFilters'
import type { SeverityLevel } from '@/types/analysis'

type Props = {
  title: string
  date: string
  flaggedCount: number
  score: number
  high: number
  medium: number
  low: number
  overallRisk: SeverityLevel
  onFilterChange?: (level: SeverityLevel | null) => void
}

export function AnalysisScoreCard({
  title,
  date,
  flaggedCount,
  score,
  high,
  medium,
  low,
  overallRisk,
  onFilterChange,
}: Props) {
  const [selectedSeverity, setSelectedSeverity] =
    useState<SeverityLevel | null>(null)

  const handleSelect = (level: SeverityLevel | null) => {
    setSelectedSeverity(level)
    onFilterChange?.(level)
  }

  const riskStyles = {
    High: {
      badge: 'bg-red-100 text-red-600',
      text: 'text-red-500',
      gradient: 'from-red-400 to-red-500',
    },
    Medium: {
      badge: 'bg-amber-100 text-amber-600',
      text: 'text-amber-500',
      gradient: 'from-amber-400 to-amber-500',
    },
    Low: {
      badge: 'bg-emerald-100 text-emerald-600',
      text: 'text-emerald-500',
      gradient: 'from-emerald-400 to-emerald-500',
    },
  }

  const styles = riskStyles[overallRisk]

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="rounded-2xl p-14 bg-white/80 border border-black/5 backdrop-blur"
    >
      {/* Top Section */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <div className="flex items-center gap-3 mb-3">
            <span
              className={`px-3 py-1.5 rounded-xl text-sm font-bold ${styles.badge}`}
            >
              {overallRisk} Risk Contract
            </span>

            <span className="text-xs text-slate-400">
              {date}
            </span>
          </div>

          <h2 className="text-2xl font-bold text-slate-900 mb-1">
            {title}
          </h2>

          <p className="text-sm text-slate-500">
            {flaggedCount} clauses flagged for review
          </p>
        </div>

        {/* Big Score */}
        <div className="text-right flex-shrink-0 ml-6">
          <div className={`text-5xl font-bold ${styles.text}`}>
            {score}
          </div>
          <div className="text-xs text-slate-400 mt-1">
            Risk Score / 100
          </div>
        </div>
      </div>

      {/* Severity Filters */}
      <div className="mb-6">
        <SeverityFilters
          counts={{
            High: high,
            Medium: medium,
            Low: low,
          }}
          selected={selectedSeverity}
          onSelect={handleSelect}
        />
      </div>

      {/* Progress Bar */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wide">
            Overall Risk Score
          </span>

          <span className={`text-sm font-bold ${styles.text}`}>
            {score}/100
          </span>
        </div>

        <div className="h-2.5 rounded-full bg-slate-100 overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${score}%` }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
            className={`h-full rounded-full bg-gradient-to-r ${styles.gradient}`}
          />
        </div>
      </div>
    </motion.div>
  )
}