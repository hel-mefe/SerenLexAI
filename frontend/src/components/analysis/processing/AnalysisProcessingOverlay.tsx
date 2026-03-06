import { useEffect, useState } from 'react'
import { Loader2, Check } from 'lucide-react'
import { motion } from 'framer-motion'

import type { AnalysisId, AnalysisStatus } from '@/types/analysis'
import type { AnalysisDetail } from '@/api/analysis/dtos'
import { useAnalysisDetail } from '@/api/analysis/hooks'

type Props = {
  analysisId: AnalysisId
  onDone: (status: AnalysisStatus) => void
}

const PHASES = [
  'Preparing document',
  'Analyzing clauses',
  'Running risk models',
  'Generating report',
]

export function AnalysisProcessingOverlay({ analysisId, onDone }: Props) {
  const [phaseIndex, setPhaseIndex] = useState(0)

  const { data } = useAnalysisDetail(analysisId, {
    refetchIntervalMs: 2500,
  })

  const status = (data as AnalysisDetail | undefined)?.status

  useEffect(() => {
    if (!status) return
    if (status === 'pending') return

    if (['completed', 'failed', 'not_contract'].includes(status)) {
      onDone(status as AnalysisStatus)
    }
  }, [status, onDone])

  useEffect(() => {
    const id = setInterval(() => {
      setPhaseIndex((current) =>
        current < PHASES.length - 1 ? current + 1 : current,
      )
    }, 2000)
    return () => clearInterval(id)
  }, [])

  return (
    <div className="flex flex-1 flex-col items-center justify-center gap-8">
      <ul className="flex flex-col gap-1.5">
        {PHASES.map((label, i) => {
          const isDone = i < phaseIndex
          const isActive = i === phaseIndex

          return (
            <motion.li
              key={label}
              initial={{ opacity: 0.6 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.2 }}
              className={`flex items-center gap-2.5 py-1.5 px-3 rounded-lg text-sm transition-colors ${
                isActive ? 'bg-brand-800 text-white' : 'text-neutral-400'
              }`}
            >
              {isDone ? (
                <Check className="h-4 w-4 shrink-0 text-neutral-400" strokeWidth={2.5} />
              ) : isActive ? (
                <Loader2 className="h-4 w-4 shrink-0 animate-spin text-white" />
              ) : (
                <span className="h-4 w-4 shrink-0 rounded-full border border-neutral-300 bg-transparent" />
              )}
              <span>{label}</span>
            </motion.li>
          )
        })}
      </ul>

      <motion.div
        animate={{ y: [0, -6, 0] }}
        transition={{
          duration: 1.2,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
        className="flex justify-center"
      >
        <svg viewBox="0 0 64 64" className="h-16 w-16">
          {/* ears */}
          <circle cx="16" cy="18" r="8" fill="#1a1a1a" />
          <circle cx="48" cy="18" r="8" fill="#1a1a1a" />
          {/* head */}
          <circle cx="32" cy="32" r="18" fill="#1a1a1a" />
          <circle cx="32" cy="32" r="14" fill="#f5f5f5" />
          {/* eyes */}
          <circle cx="26" cy="28" r="4" fill="#1a1a1a" />
          <circle cx="38" cy="28" r="4" fill="#1a1a1a" />
          {/* nose */}
          <ellipse cx="32" cy="36" rx="2" ry="2.5" fill="#1a1a1a" />
        </svg>
      </motion.div>
    </div>
  )
}

