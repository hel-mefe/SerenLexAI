import { useEffect, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'

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
    }, 2200)
    return () => clearInterval(id)
  }, [])

  const currentPhase = PHASES[phaseIndex]

  return (
    <div className="flex flex-1 flex-col items-center justify-center gap-6">
      <div className="flex justify-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 300 150"
          className="h-20 w-40"
        >
          <defs>
            <linearGradient
              id="loader-gradient"
              x1="0%"
              y1="0%"
              x2="100%"
              y2="0%"
            >
              <stop offset="0%" stopColor="#64748B" />
              <stop offset="50%" stopColor="#94A3B8" />
              <stop offset="100%" stopColor="#64748B" />
            </linearGradient>
          </defs>
          <path
            fill="none"
            stroke="url(#loader-gradient)"
            strokeWidth="15"
            strokeLinecap="round"
            strokeDasharray="300 385"
            strokeDashoffset="0"
            d="M275 75c0 31-27 50-50 50-58 0-92-100-150-100-28 0-50 22-50 50s23 50 50 50c58 0 92-100 150-100 24 0 50 19 50 50Z"
          >
            <animate
              attributeName="stroke-dashoffset"
              calcMode="spline"
              dur="3.2"
              values="685;-685"
              keySplines="0.4 0 0.2 1"
              repeatCount="indefinite"
            />
          </path>
        </svg>
      </div>

      <div className="h-6 flex items-center justify-center min-w-[12rem]">
        <AnimatePresence mode="wait">
          <motion.span
            key={currentPhase}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -6 }}
            transition={{
              duration: 0.4,
              ease: [0.4, 0, 0.2, 1],
            }}
            className="text-sm text-neutral-500"
          >
            {currentPhase}
          </motion.span>
        </AnimatePresence>
      </div>
    </div>
  )
}

