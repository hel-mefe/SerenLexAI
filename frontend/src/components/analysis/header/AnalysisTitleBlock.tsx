import { RiskBadge } from '@/components/analysis/badges/RiskBadge'

type Props = {
  title: string
  riskLevel: 'High' | 'Medium' | 'Low' | null
  status: string
  date: string
  reviewedCount: number
}

export function AnalysisTitleBlock({
  title,
  riskLevel,
  status,
  date,
  reviewedCount,
}: Props) {
  const isNotContract = status === 'not_contract'

  return (
    <div>
      <div className="flex items-center gap-2 flex-wrap">
        <h1 className="text-xl font-bold text-white leading-tight truncate max-w-lg">
          {title}
        </h1>

        {isNotContract ? (
          <span className="inline-flex items-center rounded-full border border-slate-500 bg-slate-700/80 px-2.5 py-0.5 text-xs font-semibold text-slate-200">
            Not a contract
          </span>
        ) : (
          <RiskBadge level={riskLevel ?? 'Low'} />
        )}
      </div>

      <p className="text-xs text-slate-300 mt-0.5">
        Analyzed on {date}
        {!isNotContract && reviewedCount > 0 && ` · ${reviewedCount} clauses reviewed`}
      </p>
    </div>
  )
}