import { useState } from 'react'

import { HistoryHeader } from '@/components/history/HistoryHeader'
import { HistoryFilters } from '@/components/history/HistoryFilters'
import { HistoryTimeline } from '@/components/history/HistoryTimeline'
import { HistoryEmptyState } from '@/components/history/HistoryEmptyState'

import { mockHistory } from '@/types/history'
import type { HistoryEvent } from '@/types/history'

export function HistoryPage() {
  const [filter, setFilter] = useState<'All' | HistoryEvent['type']>('All')

  const filtered =
    filter === 'All'
      ? mockHistory
      : mockHistory.filter((e) => e.type === filter)

  return (
    <div className="flex-1 flex flex-col min-w-0">
      <HistoryHeader />

      <main className="flex-1 p-8 overflow-auto space-y-6">
        <HistoryFilters
          filter={filter}
          onChange={setFilter}
        />

        {filtered.length === 0 ? (
          <HistoryEmptyState />
        ) : (
          <HistoryTimeline items={filtered} />
        )}
      </main>
    </div>
  )
}