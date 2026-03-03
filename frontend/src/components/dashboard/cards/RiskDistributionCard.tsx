export function RiskDistributionCard() {
  return (
    <div className="rounded-2xl p-6 bg-white/80 backdrop-blur border border-black/5">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-base font-bold text-slate-900">
          Risk Distribution
        </h2>

        <div className="flex items-center gap-1 p-1 rounded-lg bg-slate-100">
          <button className="px-3 py-1 text-xs font-semibold bg-white text-slate-800 rounded-md shadow-sm">
            Week
          </button>
          <button className="px-3 py-1 text-xs text-slate-500 hover:text-slate-700 rounded-md">
            Month
          </button>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3 mb-6">
        <RiskStat color="red" value="8" label="High Risk" percent="17%" />
        <RiskStat color="amber" value="15" label="Medium Risk" percent="33%" />
        <RiskStat color="emerald" value="23" label="Low Risk" percent="50%" />
      </div>

      {/* Placeholder chart */}
      <div className="h-40 flex items-end gap-2">
        {[65, 45, 80, 55, 90, 70, 85].map((h, i) => (
          <div key={i} className="flex-1 flex flex-col items-center gap-2">
            <div
              className="w-full rounded-t-lg bg-gradient-to-t from-[#1a1f2e] to-slate-500"
              style={{ height: `${h}%` }}
            />
            <span className="text-xs text-slate-400">
              {['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][i]}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

function RiskStat({
  color,
  value,
  label,
  percent,
}: {
  color: 'red' | 'amber' | 'emerald'
  value: string
  label: string
  percent: string
}) {
  return (
    <div className={`bg-${color}-500/10 rounded-xl p-4`}>
      <div className={`text-3xl font-bold text-${color}-500 mb-0.5`}>
        {value}
      </div>
      <div className="text-xs text-slate-500 font-medium mb-3">
        {label}
      </div>
      <div className="h-1.5 rounded-full bg-black/5 overflow-hidden">
        <div
          className={`h-full rounded-full bg-gradient-to-r from-${color}-500 to-${color}-400`}
          style={{ width: percent }}
        />
      </div>
    </div>
  )
}