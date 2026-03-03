function Stat({ value, label }: { value: string; label: string }) {
  return (
    <div>
      <div className="text-xl font-bold">{value}</div>
      <div className="text-xs text-white/40">{label}</div>
    </div>
  )
}

export function StatsGroup() {
  return (
    <div className="flex items-center gap-7 mb-9">
      <Stat value="98%" label="Detection Rate" />
      <Stat value="<2 min" label="Per Contract" />
      <Stat value="10K+" label="Analyzed" />
    </div>
  )
}