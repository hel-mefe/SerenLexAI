import type { SeverityLevel } from '@/types/analysis'
import { ClauseSeverityTabs } from './ClauseSeverityTabs'

type FilterValue = 'All' | SeverityLevel

type Props = {
  filter: FilterValue
  onFilterChange: (value: FilterValue) => void
}

export function ClauseSectionHeader({
  filter,
  onFilterChange,
}: Props) {
  return (
    <div className="flex items-center justify-between">
      <h3 className="text-base font-bold text-slate-900">
        Detailed Clause Analysis
      </h3>

      <ClauseSeverityTabs
        value={filter}
        onChange={onFilterChange}
      />
    </div>
  )
}