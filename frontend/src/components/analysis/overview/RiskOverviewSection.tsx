export function RiskOverviewSection() {
  return (
    <div className="grid grid-cols-3 gap-6">
      <RiskStat label="High Risk" value="4" color="red" />
      <RiskStat label="Medium Risk" value="5" color="amber" />
      <RiskStat label="Low Risk" value="3" color="emerald" />
    </div>
  )
}

function RiskStat({
  label,
  value,
  color,
}: {
  label: string
  value: string
  color: 'red' | 'amber' | 'emerald'
}) {
  return (
    <div className={`rounded-2xl p-6 bg-${color}-50 border border-${color}-100`}>
      <div className={`text-3xl font-bold text-${color}-600`}>
        {value}
      </div>
      <div className="text-sm text-slate-500 mt-2">
        {label}
      </div>
    </div>
  )
}