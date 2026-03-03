import { Search } from 'lucide-react'
import type { SeverityLevel } from '@/types/analysis'

type FilterValue = 'All' | SeverityLevel

type Props = {
  search: string
  onSearchChange: (value: string) => void
  filter: FilterValue
  onFilterChange: (value: FilterValue) => void
}

export function AnalysesFiltersBar({
  search,
  onSearchChange,
  filter,
  onFilterChange,
}: Props) {
  const filters: FilterValue[] = [
    'All',
    'High',
    'Medium',
    'Low',
  ]

  return (
    <div className="rounded-2xl p-5 mb-6 bg-white/85 backdrop-blur border border-black/5">
      <div className="flex items-center justify-between gap-4">
        {/* Search */}
        <div className="flex-1 max-w-md relative">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
          <input
            value={search}
            onChange={(e) =>
              onSearchChange(e.target.value)
            }
            placeholder="Search contracts..."
            className="w-full pl-10 pr-4 py-2.5 rounded-xl text-sm bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-slate-300 transition-all"
          />
        </div>

        {/* Severity Filter */}
        <div className="flex items-center gap-2">
          {filters.map((item) => {
            const active = filter === item
            return (
              <button
                key={item}
                onClick={() => onFilterChange(item)}
                className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
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
    </div>
  )
}