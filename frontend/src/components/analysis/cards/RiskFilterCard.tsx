type Props = {
  level: 'High' | 'Medium' | 'Low'
  value: number
  color: 'red' | 'amber' | 'emerald'
  onClick?: () => void
}

export function RiskFilterCard({
  level,
  value,
  color,
  onClick,
}: Props) {
  return (
    <button
      onClick={onClick}
      className={`bg-${color}-50 rounded-xl p-5 text-left transition hover:shadow-md`}
    >
      <div className={`text-3xl font-bold text-${color}-500 mb-1`}>
        {value}
      </div>

      <div className="text-xs text-slate-500 font-medium">
        {level} Risk
      </div>

      <div className="text-xs text-slate-400 mt-1">
        Click to filter
      </div>
    </button>
  )
}