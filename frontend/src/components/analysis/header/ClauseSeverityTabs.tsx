import type { SeverityLevel } from '@/types/analysis'

type FilterValue = 'All' | SeverityLevel

type Props = {
  value: FilterValue
  onChange: (value: FilterValue) => void
}

export function ClauseSeverityTabs({
  value,
  onChange,
}: Props) {
  const tabs: FilterValue[] = ['All', 'High', 'Medium', 'Low']

  return (
    <div className="flex items-center gap-2">
      {tabs.map((tab) => {
        const isActive = value === tab

        return (
          <button
            key={tab}
            onClick={() => onChange(tab)}
            className={`
              px-3 py-1.5 rounded-lg text-xs font-semibold transition-all whitespace-nowrap
              ${
                isActive
                  ? 'bg-slate-900 text-white shadow-md'
                  : 'bg-white/80 text-slate-600 hover:bg-white border border-slate-200'
              }
            `}
          >
            {tab}
          </button>
        )
      })}
    </div>
  )
}