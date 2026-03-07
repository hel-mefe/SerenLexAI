type Props = {
  level: 'High' | 'Medium' | 'Low'
}

export function RiskBadge({ level }: Props) {
  const styles =
    level === 'High'
      ? 'bg-risk-high-bg text-risk-high'
      : level === 'Medium'
      ? 'bg-risk-medium-bg text-risk-medium'
      : 'bg-risk-low-bg text-risk-low'

  return (
    <span
      className={`px-2.5 py-1 rounded-full text-xs font-bold whitespace-nowrap ${styles}`}
    >
      {level} Risk
    </span>
  )
}