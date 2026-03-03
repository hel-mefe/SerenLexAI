import { useState } from 'react'

import { HistoryHeader } from '@/components/history/HistoryHeader'
import { HistoryFilters } from '@/components/history/HistoryFilters'
import { HistoryTimeline } from '@/components/history/HistoryTimeline'
import { HistoryEmptyState } from '@/components/history/HistoryEmptyState'
import type { HistoryEvent } from '@/types/history'
import { useHistoryEvents } from '@/api/history/hooks'

export function HistoryPage() {
  const [filter, setFilter] = useState<'All' | HistoryEvent['type']>('All')

  const {
    data,
    isLoading,
    isError,
    refetch,
  } = useHistoryEvents({
    type: filter === 'All' ? 'All' : filter,
  })

  const items = data?.items ?? []

  return (
    <div className="flex-1 flex flex-col min-w-0">
      <HistoryHeader />

      <main className="flex-1 p-8 overflow-auto space-y-6">
        <HistoryFilters
          filter={filter}
          onChange={setFilter}
        />

        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-16 text-center">
            <div className="w-10 h-10 rounded-full border-2 border-slate-300 border-t-transparent animate-spin" />
            <p className="mt-4 text-sm text-slate-500">
              Loading your recent activity…
            </p>
          </div>
        ) : isError ? (
          <div className="rounded-2xl border border-red-100 bg-red-50/60 px-6 py-5 text-left max-w-lg">
            <p className="text-sm font-semibold text-red-600">
              Unable to load history
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
        ) : items.length === 0 ? (
          <HistoryEmptyState />
        ) : (
          <HistoryTimeline items={items} />
        )}
      </main>
    </div>
  )
}