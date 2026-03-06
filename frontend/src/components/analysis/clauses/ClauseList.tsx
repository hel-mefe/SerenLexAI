import type { SeverityLevel } from '@/types/analysis'
import type { ClauseItem } from '@/types/clause'
import { useClausesByAnalysis } from '@/api/clause/hooks'
import { ClauseCard } from '../cards/ClauseCard'

type FilterValue = 'All' | SeverityLevel

type Props = {
  analysisId: string | undefined
  filter: FilterValue
}

export function ClauseList({ analysisId, filter }: Props) {
  const severity = filter === 'All' ? undefined : filter

  const {
    data,
    isLoading,
    isError,
    refetch,
  } = useClausesByAnalysis({
    analysisId,
    severity,
  })

  const clauses: ClauseItem[] = data?.items ?? []

  if (isLoading) {
    return (
      <div className="py-16 text-center text-slate-400 text-sm">
        Loading clauses…
      </div>
    )
  }

  if (isError) {
    return (
      <div className="py-16 text-center text-slate-400 text-sm">
        Unable to load clauses.
        <button
          type="button"
          onClick={() => refetch()}
          className="ml-2 text-xs font-semibold text-slate-600 underline"
        >
          Try again
        </button>
      </div>
    )
  }

  if (clauses.length === 0) {
    return (
      <div className="py-16 text-center text-slate-400 text-sm">
        No clauses found for{' '}
        <span className="font-semibold capitalize">{filter}</span>{' '}
        severity.
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {clauses.map((clause) => (
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