import { Search } from 'lucide-react'
import type { SeverityLevel } from '@/types/analysis'

type SeverityFilterValue = 'All' | SeverityLevel
type StatusFilterValue = 'All' | 'completed' | 'pending' | 'failed' | 'not_contract'

type Props = {
  search: string
  onSearchChange: (value: string) => void
  filter: SeverityFilterValue
  onFilterChange: (value: SeverityFilterValue) => void
  statusFilter?: StatusFilterValue
  onStatusFilterChange?: (value: StatusFilterValue) => void
}

export function AnalysesFiltersBar({
  search,
  onSearchChange,
  filter,
  onFilterChange,
  statusFilter = 'All',
  onStatusFilterChange,
}: Props) {
  const severityFilters: SeverityFilterValue[] = [
    'All',
    'High',
    'Medium',
    'Low',
  ]

  const statusFilters: StatusFilterValue[] = [
    'All',
    'completed',
    'pending',
    'failed',
    'not_contract',
  ]

  return (
    <div className="rounded-2xl p-5 mb-6 bg-white/85 backdrop-blur border border-black/5">
      {/* Search row */}
      <div className="flex items-center gap-4 mb-3">
        <div className="flex-1 relative">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
          <input
            value={search}
            onChange={(e) =>
              onSearchChange(e.target.value)
            }
            placeholder="Search contracts..."
            className="w-full max-w-[460px] pl-10 pr-4 py-2.5 rounded-xl text-sm bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-slate-300 transition-all"
          />
        </div>
      </div>

      {/* Filters row: Severity + Status on left */}
      <div className="flex flex-wrap items-center gap-8 mt-6">
        <div className="flex items-center gap-2">
          <span className="text-[11px] font-semibold uppercase tracking-wide text-slate-400">
            Severity
          </span>
          <div className="flex items-center gap-2">
            {severityFilters.map((item) => {
              const active = filter === item
              return (
                <button
                  key={item}
                  onClick={() => onFilterChange(item)}
                  className={`px-3 py-1.5 rounded-xl text-[11px] font-semibold transition-all ${
                    active
                    ? 'bg-slate-900 text-white shadow-lg'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
                >
                  {item}
                </button>
              )
            })}
          </div>
        </div>

        {onStatusFilterChange && (
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-semibold uppercase tracking-wide text-slate-400">
              Status
            </span>
            <div className="flex items-center gap-2">
              {statusFilters.map((item) => {
                const active = statusFilter === item
                const label =
                  item === 'completed'
                    ? 'Done'
                    : item === 'pending'
                      ? 'Processing'
                      : item === 'failed'
                        ? 'Failed'
                        : item === 'not_contract'
                          ? 'Not a contract'
                          : 'All'
                return (
                  <button
                    key={item}
                    onClick={() => onStatusFilterChange(item)}
                    className={`px-3 py-1.5 rounded-xl text-[11px] font-semibold transition-all ${
                      active
                        ? 'bg-slate-900 text-white shadow-lg'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    {label}
                  </button>
                )
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}