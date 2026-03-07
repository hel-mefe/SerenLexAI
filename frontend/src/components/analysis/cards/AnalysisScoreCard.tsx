import { motion } from 'framer-motion'
import { useState } from 'react'
import { SeverityFilters } from '@/components/analysis/overview/SeverityFilters'
import type { SeverityLevel } from '@/types/analysis'

type Props = {
  title: string
  date: string
  flaggedCount: number
  high: number
  medium: number
  low: number
  overallRisk: SeverityLevel | null
  status: string
  onFilterChange?: (level: SeverityLevel | null) => void
}

export function AnalysisScoreCard({
  title,
  date,
  flaggedCount,
  high,
  medium,
  low,
  overallRisk,
  status,
  onFilterChange,
}: Props) {
  const [selectedSeverity, setSelectedSeverity] =
    useState<SeverityLevel | null>(null)

  const handleSelect = (level: SeverityLevel | null) => {
    setSelectedSeverity(level)
    onFilterChange?.(level)
  }

  const isNotContract = status === 'not_contract'

  const riskStyles: Record<
    SeverityLevel,
    { badge: string; text: string }
  > = {
    High: {
      badge: 'bg-risk-high-bg text-risk-high',
      text: 'text-risk-high',
    },
    Medium: {
      badge: 'bg-risk-medium-bg text-risk-medium',
      text: 'text-risk-medium',
    },
    Low: {
      badge: 'bg-risk-low-bg text-risk-low',
      text: 'text-risk-low',
    },
  }

  const notContractStyles = {
    badge: 'bg-slate-100 text-slate-600',
    text: 'text-slate-500',
  }

  const displayRisk = isNotContract ? null : (overallRisk ?? 'Low')
  const styles = displayRisk
    ? riskStyles[displayRisk]
    : notContractStyles

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="rounded-2xl p-14 bg-white/80 border border-black/5 backdrop-blur"
    >
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-3 mb-3">
            <span
              className={`px-3 py-1.5 rounded-xl text-sm font-bold ${styles.badge}`}
            >
              {isNotContract ? 'Not a contract' : `${displayRisk} Risk Contract`}
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
      </div>

      {!isNotContract && (
        <div className="mt-6">
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
      )}
    </motion.div>
  )
}
