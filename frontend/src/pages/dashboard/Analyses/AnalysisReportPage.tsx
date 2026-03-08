import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useState } from 'react'
import { ArrowLeft } from 'lucide-react'

import { AnalysisTopBar } from '@/components/analysis/header/AnalysisTopBar'
import { AnalysisScoreCard } from '@/components/analysis/cards/AnalysisScoreCard'
import { ClauseSectionHeader } from '@/components/analysis/header/ClauseSectionHeader'
import { ClauseList } from '@/components/analysis/clauses/ClauseList'
import { AnalysisProcessingOverlay } from '@/components/analysis/processing/AnalysisProcessingOverlay'

import type { SeverityLevel, AnalysisId } from '@/types/analysis'
import type { AnalysisDetail } from '@/api/analysis/dtos'
import { useAnalysisDetail } from '@/api/analysis/hooks'

type FilterValue = 'All' | SeverityLevel

export function AnalysisReportPage() {
  const { analysisId } = useParams<{ analysisId: string }>()
  const navigate = useNavigate()

  const [severityFilter, setSeverityFilter] =
    useState<FilterValue>('All')

  const { data, isLoading, isError } = useAnalysisDetail(
    analysisId as AnalysisId | undefined,
    { refetchIntervalMs: 2500 },
  )

  const handleFilter = (level: SeverityLevel | null) => {
    if (!level) {
      setSeverityFilter('All')
      return
    }
    setSeverityFilter(level)
  }

  if (isError || !data) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <div className="text-sm text-red-500">
          Unable to load analysis report.
        </div>
      </div>
    )
  }

  const analysis = data as AnalysisDetail

  if (isLoading || analysis.status === 'pending') {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
        className="relative flex-1 flex flex-col min-h-[60vh]"
      >
        <div className="absolute top-0 left-0">
          <button
            onClick={() => navigate('/dashboard/analyses')}
            className="flex items-center gap-2 p-2 rounded-lg text-neutral-600 hover:text-neutral-900 hover:bg-neutral-200/60 transition-colors"
            aria-label="Back to analyses"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
        </div>

        <div className="flex-1 flex">
          <AnalysisProcessingOverlay
            analysisId={analysisId as AnalysisId}
            onDone={() => { /* no-op */ }}
          />
        </div>
      </motion.div>
    )
  }

  const formattedDate = analysis.createdAt.toLocaleString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })

  const isNotContract = analysis.status === 'not_contract'

  if (isNotContract) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="space-y-10"
      >
        <div className="mx-14">
          <AnalysisTopBar
            analysisId={analysis.id}
            title={analysis.title}
            date={formattedDate}
            reviewedCount={0}
            overallRisk={null}
            status={analysis.status}
            sourceType={analysis.sourceType}
            originalFilename={analysis.originalFilename}
          />
        </div>

        <div className="mx-14">
          <div className="max-w-lg mx-auto flex flex-col items-center justify-center py-20 text-center">
            <div className="rounded-2xl border border-slate-200 bg-slate-50/80 px-8 py-10">
            <p className="text-lg font-semibold text-slate-800">
              This document was classified as not a contract.
            </p>
            <p className="text-sm text-slate-500 mt-2">
              No risk assessment, score, or clause analysis is available. Only contract documents receive a full analysis.
            </p>
            </div>
          </div>
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="space-y-10"
    >
      {/* 🔹 Top Section */}
      <div className="space-y-6 mx-14">
        <AnalysisTopBar
          analysisId={analysis.id}
          title={analysis.title}
          date={formattedDate}
          reviewedCount={analysis.flaggedCount}
          overallRisk={analysis.overallRisk ?? 'Low'}
          status={analysis.status}
          sourceType={analysis.sourceType}
          originalFilename={analysis.originalFilename}
        />

        <AnalysisScoreCard
          title={analysis.title}
          date={formattedDate}
          flaggedCount={analysis.flaggedCount}
          high={analysis.high}
          medium={analysis.medium}
          low={analysis.low}
          overallRisk={analysis.overallRisk ?? 'Low'}
          status={analysis.status}
          onFilterChange={handleFilter}
        />
      </div>

      {/* 🔹 Main Content */}
      <div className="ml-14 space-y-8">
        <ClauseSectionHeader
          filter={severityFilter}
          onFilterChange={setSeverityFilter}
        />

        <ClauseList
          analysisId={analysisId}
          filter={severityFilter}
        />
      </div>
    </motion.div>
  )
}