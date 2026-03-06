import { useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useState } from 'react'

import { AnalysisTopBar } from '@/components/analysis/header/AnalysisTopBar'
import { AnalysisScoreCard } from '@/components/analysis/cards/AnalysisScoreCard'
import { ClauseSectionHeader } from '@/components/analysis/header/ClauseSectionHeader'
import { ClauseList } from '@/components/analysis/clauses/ClauseList'
import { ClauseNavigation } from '@/components/analysis/sidebar/ClauseNavigation'

import type { SeverityLevel, AnalysisId } from '@/types/analysis'
import { useAnalysisDetail } from '@/api/analysis/hooks'

type FilterValue = 'All' | SeverityLevel

export function AnalysisReportPage() {
  const { analysisId } = useParams<{ analysisId: string }>()

  const [severityFilter, setSeverityFilter] =
    useState<FilterValue>('All')

  const { data, isLoading, isError } = useAnalysisDetail(
    analysisId as AnalysisId | undefined,
  )

  const handleScoreFilter = (level: SeverityLevel | null) => {
    if (!level) {
      setSeverityFilter('All')
      return
    }

    setSeverityFilter(level)
  }

  if (isLoading) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <div className="text-sm text-slate-500">
          Loading analysis report…
        </div>
      </div>
    )
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

  const formattedDate = data.createdAt.toLocaleString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="space-y-10"
    >
      {/* 🔹 Top Section */}
      <div className="space-y-6 mx-14">
        <AnalysisTopBar analysisId={analysisId} />

        <AnalysisScoreCard
          title={data.title}
          date={formattedDate}
          flaggedCount={data.flaggedCount}
          score={data.score ?? 0}
          high={data.high}
          medium={data.medium}
          low={data.low}
          overallRisk={data.overallRisk ?? 'Low'}
          onFilterChange={handleScoreFilter}
        />
      </div>

      {/* 🔹 Main Content Grid */}
      <div className="grid grid-cols-4 gap-10 ml-14">
        {/* Main Report Content */}
        <div className="col-span-4 xl:col-span-3 space-y-8">
          {/* Clause Filters Header */}
          <ClauseSectionHeader
            filter={severityFilter}
            onFilterChange={setSeverityFilter}
          />

          {/* Clause List */}
          <ClauseList
            analysisId={analysisId}
            filter={severityFilter}
          />
        </div>

        {/* Sticky Clause Navigation */}
        <div className="hidden xl:block">
          <div className="sticky top-24">
            <ClauseNavigation />
          </div>
        </div>
      </div>
    </motion.div>
  )
}