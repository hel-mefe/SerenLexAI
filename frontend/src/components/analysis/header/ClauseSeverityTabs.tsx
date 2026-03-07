import type { SeverityLevel } from '@/types/analysis'
import clsx from 'clsx'

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
            className={clsx(
              'px-3 py-1.5 rounded-lg text-xs font-semibold transition-all whitespace-nowrap',
              isActive
                ? 'bg-neutral-700 text-white'
                : 'text-neutral-600 hover:bg-neutral-100'
            )}
          >
            {tab}
          </button>
        )
      })}
    </div>
  )
}