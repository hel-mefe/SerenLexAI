import { useState, useMemo } from 'react'
import { motion } from 'framer-motion'

import { AnalysesHeader } from '@/components/analysis/header/AnalysesHeader'
import { AnalysesFiltersBar } from '@/components/analysis/filters/AnalysesFiltersBar'
import { AnalysesTable } from '@/components/analysis/tables/AnalysesTable'
import { Pagination } from '@/components/analysis/tables/Pagination'

import type { SeverityLevel } from '@/types/analysis'
import { mockAnalyses } from './mock'

type FilterValue = 'All' | SeverityLevel

export function AnalysesPage() {
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState<FilterValue>('All')
  const [page, setPage] = useState(1)

  const filteredData = useMemo(() => {
    return mockAnalyses
      .filter((item: any) =>
        item.name.toLowerCase().includes(search.toLowerCase())
      )
      .filter((item: any) =>
        filter === 'All' ? true : item.risk === filter
      )
  }, [search, filter])

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="flex-1 flex flex-col min-w-0"
    >
      <AnalysesHeader total={filteredData.length} />

      <main className="flex-1 p-8 overflow-auto">
        <AnalysesFiltersBar
          search={search}
          onSearchChange={setSearch}
          filter={filter}
          onFilterChange={setFilter}
        />

        <AnalysesTable data={filteredData} />

        <Pagination page={page} onChange={setPage} />
      </main>
    </motion.div>
  )
}