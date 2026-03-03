type ClauseNavItem = {
  id: string
  title: string
  severity: 'High' | 'Medium' | 'Low'
}

const mockNav: ClauseNavItem[] = [
  { id: '1', title: 'Limitation of Liability', severity: 'High' },
  { id: '2', title: 'Termination', severity: 'Medium' },
  { id: '3', title: 'IP Ownership', severity: 'High' },
  { id: '4', title: 'Payment Terms', severity: 'Low' },
]

export function ClauseNavigation() {
  return (
    <div className="sticky top-24 space-y-3">
      <h3 className="text-sm font-bold text-slate-900">
        Flagged Clauses
      </h3>

      <div className="space-y-2">
        {mockNav.map((item) => (
          <button
            key={item.id}
            className="w-full text-left px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition"
          >
            {item.title}
          </button>
        ))}
      </div>
    </div>
  )
}