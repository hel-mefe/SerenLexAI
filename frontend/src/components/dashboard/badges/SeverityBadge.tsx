export function SeverityBadge({
  severity,
}: {
  severity: 'High' | 'Medium' | 'Low'
}) {
  const styles =
    severity === 'High'
      ? 'bg-red-100 text-red-600'
      : severity === 'Medium'
      ? 'bg-amber-100 text-amber-600'
      : 'bg-emerald-100 text-emerald-600'

  return (
    <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${styles}`}>
      {severity}
    </span>
  )
}