type Props = {
  level: 'High' | 'Medium' | 'Low'
}

export function RiskBadge({ level }: Props) {
  const styles =
    level === 'High'
      ? 'bg-red-100 text-red-600'
      : level === 'Medium'
      ? 'bg-amber-100 text-amber-600'
      : 'bg-emerald-100 text-emerald-600'

  return (
    <span
      className={`px-2.5 py-1 rounded-full text-xs font-bold whitespace-nowrap ${styles}`}
    >
      {level} Risk
    </span>
  )
}