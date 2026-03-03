export function RiskSummaryBanner() {
  return (
    <div className="rounded-2xl p-6 bg-red-50 border border-red-100">
      <h3 className="text-lg font-bold text-red-600 mb-1">
        Overall Risk: High
      </h3>
      <p className="text-sm text-red-500">
        Several liability and termination clauses expose your organization
        to elevated financial and operational risk.
      </p>
    </div>
  )
}