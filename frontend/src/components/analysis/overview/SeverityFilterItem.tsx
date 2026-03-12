import type { SeverityLevel } from '@/types/analysis'
import clsx from 'clsx'

type Props = {
  level: SeverityLevel
  value: number
  selected?: boolean
  onClick?: () => void
}

/** White cards with risk-colored borders for each severity level */
const CARD_STYLES: Record<SeverityLevel, { border: string; ring: string; text: string }> = {
  High: {
    border: 'border-risk-high',
    ring: 'ring-risk-high',
    text: 'text-risk-high',
  },
  Medium: {
    border: 'border-risk-medium',
    ring: 'ring-risk-medium',
    text: 'text-risk-medium',
  },
  Low: {
    border: 'border-risk-low',
    ring: 'ring-risk-low',
    text: 'text-risk-low',
  },
}

export function SeverityFilterItem({
  level,
  value,
  selected,
  onClick,
}: Props) {
  const { border, ring, text } = CARD_STYLES[level]

  return (
    <button
      onClick={onClick}
      className={clsx(
        'rounded-xl p-5 text-left transition border-2 bg-white hover:shadow-md',
        border,
        selected && 'ring-2 ring-offset-2 ring-offset-white',
        selected && ring
      )}
    >
      <div className={clsx('text-3xl font-bold mb-1', text)}>
        {value}
      </div>

      <div className="text-xs font-medium text-neutral-600">
        {level} Risk
      </div>

      <div className="text-xs mt-1 text-neutral-500">
        {selected ? 'Filtered' : 'Click to filter'}
      </div>
    </button>
  )
}