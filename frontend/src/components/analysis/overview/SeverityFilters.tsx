import type { SeverityLevel } from '@/types/analysis'
import { SeverityFilterItem } from './SeverityFilterItem'

type Props = {
  counts: Record<SeverityLevel, number>
  selected?: SeverityLevel | null
  onSelect?: (level: SeverityLevel | null) => void
}

export function SeverityFilters({
  counts,
  selected,
  onSelect,
}: Props) {
  return (
    <div className="grid grid-cols-3 gap-4">
      <SeverityFilterItem
        level="High"
        value={counts.High}
        selected={selected === 'High'}
        onClick={() =>
          onSelect?.(selected === 'High' ? null : 'High')
        }
      />

      <SeverityFilterItem
        level="Medium"
        value={counts.Medium}
        selected={selected === 'Medium'}
        onClick={() =>
          onSelect?.(selected === 'Medium' ? null : 'Medium')
        }
      />

      <SeverityFilterItem
        level="Low"
        value={counts.Low}
        selected={selected === 'Low'}
        onClick={() =>
          onSelect?.(selected === 'Low' ? null : 'Low')
        }
      />
    </div>
  )
}