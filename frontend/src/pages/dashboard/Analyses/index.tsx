import { useMemo } from 'react'
import { motion } from 'framer-motion'

import { AnalysesHeader } from '@/components/analysis/header/AnalysesHeader'
import { AnalysesFiltersBar } from '@/components/analysis/filters/AnalysesFiltersBar'
import { AnalysesTable } from '@/components/analysis/tables/AnalysesTable'
import { Pagination } from '@/components/analysis/tables/Pagination'

import type { AnalysisItem, AnalysisStatus, SeverityLevel } from '@/types/analysis'
import { useAnalysesList } from '@/api/analysis/hooks'
import {
  useAnalysisFiltersStore,
  type SeverityFilterValue,
} from '@/store/analysisFiltersStore'

const PAGE_SIZE = 10

export function AnalysesPage() {
  const {
    search,
    severity,
    status,
    page,
    setSearch,
    setSeverity,
    setStatus,
    setPage,
  } = useAnalysisFiltersStore()

  const {
    data,
    isLoading,
    isError,
    refetch,
  } = useAnalysesList({
    search,
    filter: severity,
    page,
    pageSize: PAGE_SIZE,
  })

  const items = (data?.items ?? []) as AnalysisItem[]

  const filteredItems = useMemo(() => {
    if (status === 'All') return items
    return items.filter((item) => item.status === status)
  }, [items, status])

  const total = filteredItems.length

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="flex-1 flex flex-col min-w-0"
    >
      <AnalysesHeader total={total} />

      <main className="flex-1 p-8 overflow-auto">
        <AnalysesFiltersBar
          search={search}
          onSearchChange={setSearch}
          filter={severity as SeverityFilterValue}
          onFilterChange={setSeverity}
          statusFilter={status}
          onStatusFilterChange={setStatus as (value: 'All' | AnalysisStatus) => void}
        />

        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div className="w-10 h-10 rounded-full border-2 border-slate-300 border-t-transparent animate-spin" />
            <p className="mt-4 text-sm text-slate-500">
              Loading analyses…
            </p>
          </div>
        ) : isError ? (
          <div className="mt-6 rounded-2xl border border-red-100 bg-red-50/60 px-6 py-5 text-left max-w-lg">
            <p className="text-sm font-semibold text-red-600">
              Unable to load analyses
            </p>
            <p className="mt-1 text-xs text-red-500">
              Please check your connection and try again.
            </p>
            <button
              type="button"
              onClick={() => refetch()}
              className="mt-4 inline-flex items-center rounded-xl bg-gradient-to-br from-[#1a1f2e] to-[#2d3550] px-3 py-1.5 text-xs font-semibold text-white shadow-sm hover:shadow-md transition-shadow"
            >
              Try again
            </button>
          </div>
        ) : (
          <>
            <AnalysesTable data={filteredItems} />
            <Pagination page={page} onChange={setPage} />
          </>
        )}
      </main>
    </motion.div>
  )
}