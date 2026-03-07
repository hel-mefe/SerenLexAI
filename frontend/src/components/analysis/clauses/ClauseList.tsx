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

  const emptyStateClass = 'py-16 text-center text-sm text-slate-500'

  if (isLoading) {
    return (
      <div className={emptyStateClass}>
        Loading clauses…
      </div>
    )
  }

  if (isError) {
    return (
      <div className={emptyStateClass}>
        Unable to load clauses.
        <button
          type="button"
          onClick={() => refetch()}
          className="ml-2 text-xs font-semibold underline text-slate-600 hover:text-slate-800"
        >
          Try again
        </button>
      </div>
    )
  }

  if (clauses.length === 0) {
    return (
      <div className={emptyStateClass}>
        No clauses found for{' '}
        <span className="font-semibold text-slate-700 capitalize">{filter}</span> severity.
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {clauses.map((clause) => (
        <ClauseCard
          key={clause.id}
          title={clause.title}
          clauseType={clause.clauseType ?? null}
          severity={clause.severity}
          originalText={clause.originalText}
          riskExplanation={clause.riskExplanation}
          recommendation={clause.recommendation}
        />
      ))}
    </div>
  )
}