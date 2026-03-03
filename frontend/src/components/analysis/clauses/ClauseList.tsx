import type { SeverityLevel } from '@/types/analysis'
import { ClauseCard } from '../cards/ClauseCard'

type FilterValue = 'All' | SeverityLevel

interface Clause {
  id: string
  title: string
  severity: SeverityLevel
  originalText: string
  riskExplanation: string
  recommendation: string
}

// Mock data — replace with real data source (API/props/context)
const MOCK_CLAUSES: Clause[] = [
  {
    id: '1',
    title: 'Unlimited Liability Clause',
    severity: 'High',
    originalText: 'The service provider shall bear unlimited liability for any damages arising from the service.',
    riskExplanation: 'Unlimited liability exposes your company to uncapped financial risk in the event of a dispute or failure.',
    recommendation: 'Negotiate a liability cap equal to the total contract value or 12 months of fees.',
  },
  {
    id: '2',
    title: 'Auto-Renewal Clause',
    severity: 'Medium',
    originalText: 'This agreement shall automatically renew for successive one-year terms unless terminated 90 days prior.',
    riskExplanation: 'The 90-day termination window is unusually long and may cause unintended renewals.',
    recommendation: 'Request a reduction to a 30-day notice period with explicit written confirmation of renewal.',
  },
  {
    id: '3',
    title: 'Intellectual Property Assignment',
    severity: 'High',
    originalText: 'All work product created under this agreement is the sole property of the client.',
    riskExplanation: 'Broad IP assignment may include pre-existing tools and frameworks owned by your company.',
    recommendation: 'Carve out pre-existing IP and limit assignment to work product created solely for this engagement.',
  },
  {
    id: '4',
    title: 'Governing Law',
    severity: 'Low',
    originalText: 'This agreement shall be governed by the laws of the State of Delaware.',
    riskExplanation: 'Jurisdiction may require travel or legal representation in an unfamiliar state.',
    recommendation: 'Negotiate for jurisdiction in your operating state or agree to remote arbitration.',
  },
]

type Props = {
  filter: FilterValue
}

export function ClauseList({ filter }: Props) {
  const filtered = filter === 'All'
    ? MOCK_CLAUSES
    : MOCK_CLAUSES.filter((clause) => clause.severity === filter)

  if (filtered.length === 0) {
    return (
      <div className="py-16 text-center text-slate-400 text-sm">
        No clauses found for <span className="font-semibold capitalize">{filter}</span> severity.
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {filtered.map((clause) => (
        <ClauseCard
          key={clause.id}
          title={clause.title}
          severity={clause.severity}
          originalText={clause.originalText}
          riskExplanation={clause.riskExplanation}
          recommendation={clause.recommendation}
        />
      ))}
    </div>
  )
}