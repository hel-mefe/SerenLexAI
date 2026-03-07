import type { SeverityLevel } from '@/types/analysis'
import clsx from 'clsx'

type Props = {
  level: SeverityLevel
  value: number
  selected?: boolean
  onClick?: () => void
}

/** Darker gradients aligned with brand (Deep Trust Navy); risk tint over brand-800/700 */
const CARD_STYLES: Record<SeverityLevel, { border: string; ring: string; gradient: string; text: string; subtext: string }> = {
  High: {
    border: 'border-risk-high',
    ring: 'ring-risk-high',
    gradient: 'linear-gradient(135deg, #2A1518 0%, #161B27 40%, #1A1F2E 70%, #25181A 100%)',
    text: 'text-white',
    subtext: 'text-slate-300',
  },
  Medium: {
    border: 'border-risk-medium',
    ring: 'ring-risk-medium',
    gradient: 'linear-gradient(135deg, #2A2415 0%, #161B27 40%, #1A1F2E 70%, #26200F 100%)',
    text: 'text-white',
    subtext: 'text-slate-300',
  },
  Low: {
    border: 'border-risk-low',
    ring: 'ring-risk-low',
    gradient: 'linear-gradient(135deg, #0F2A1F 0%, #161B27 40%, #1A1F2E 70%, #0F241C 100%)',
    text: 'text-white',
    subtext: 'text-slate-300',
  },
}

export function SeverityFilterItem({
  level,
  value,
  selected,
  onClick,
}: Props) {
  const { border, ring, gradient, text, subtext } = CARD_STYLES[level]

  return (
    <button
      onClick={onClick}
      className={clsx(
        'rounded-xl p-5 text-left transition border-2 hover:shadow-md',
        border,
        selected && 'ring-2 ring-offset-2 ring-offset-white',
        selected && ring
      )}
      style={{ background: gradient }}
    >
      <div className={clsx('text-3xl font-bold mb-1', text)}>
        {value}
      </div>

      <div className={clsx('text-xs font-medium', subtext)}>
        {level} Risk
      </div>

      <div className={clsx('text-xs mt-1', subtext)}>
        {selected ? 'Filtered' : 'Click to filter'}
      </div>
    </button>
  )
}