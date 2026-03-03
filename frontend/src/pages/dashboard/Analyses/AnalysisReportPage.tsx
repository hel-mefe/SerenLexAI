import { useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useState } from 'react'

import { AnalysisTopBar } from '@/components/analysis/header/AnalysisTopBar'
import { AnalysisScoreCard } from '@/components/analysis/cards/AnalysisScoreCard'
import { ClauseSectionHeader } from '@/components/analysis/header/ClauseSectionHeader'
import { ClauseList } from '@/components/analysis/clauses/ClauseList'
import { ClauseNavigation } from '@/components/analysis/sidebar/ClauseNavigation'

import type { SeverityLevel } from '@/types/analysis'

type FilterValue = 'All' | SeverityLevel

export function AnalysisReportPage() {
  const { analysisId } = useParams<{ analysisId: string }>()

  const [severityFilter, setSeverityFilter] =
    useState<FilterValue>('All')

  const handleScoreFilter = (level: SeverityLevel | null) => {
    if (!level) {
      setSeverityFilter('All')
      return
    }

    setSeverityFilter(level)
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
        <AnalysisTopBar analysisId={analysisId} />

        <AnalysisScoreCard
          title="Service Agreement — Acme Corp"
          date="Dec 18, 2024 · 14:32"
          flaggedCount={12}
          score={84}
          high={4}
          medium={5}
          low={3}
          overallRisk="High"
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
          <ClauseList filter={severityFilter} />
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