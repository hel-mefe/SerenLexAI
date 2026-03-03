import type { SeverityLevel } from '@/types/analysis'
import clsx from 'clsx'

type Props = {
  level: SeverityLevel
  value: number
  selected?: boolean
  onClick?: () => void
}

export function SeverityFilterItem({
  level,
  value,
  selected,
  onClick,
}: Props) {
  const colorMap = {
    High: {
      bg: 'bg-red-50',
      text: 'text-red-500',
      border: 'border-red-200',
      active: 'ring-2 ring-red-400',
    },
    Medium: {
      bg: 'bg-amber-50',
      text: 'text-amber-500',
      border: 'border-amber-200',
      active: 'ring-2 ring-amber-400',
    },
    Low: {
      bg: 'bg-emerald-50',
      text: 'text-emerald-500',
      border: 'border-emerald-200',
      active: 'ring-2 ring-emerald-400',
    },
  }

  const styles = colorMap[level]

  return (
    <button
      onClick={onClick}
      className={clsx(
        'rounded-xl p-5 text-left transition border',
        styles.bg,
        styles.border,
        selected ? styles.active : 'hover:shadow-md'
      )}
    >
      <div className={clsx('text-3xl font-bold mb-1', styles.text)}>
        {value}
      </div>

      <div className="text-xs text-slate-500 font-medium">
        {level} Risk
      </div>

      <div className="text-xs text-slate-400 mt-1">
        {selected ? 'Filtered' : 'Click to filter'}
      </div>
    </button>
  )
}