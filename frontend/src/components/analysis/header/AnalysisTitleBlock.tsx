import { RiskBadge } from '@/components/analysis/badges/RiskBadge'

type Props = {
  title: string
  riskLevel: 'High' | 'Medium' | 'Low'
  date: string
  reviewedCount: number
}

export function AnalysisTitleBlock({
  title,
  riskLevel,
  date,
  reviewedCount,
}: Props) {
  return (
    <div>
      <div className="flex items-center gap-2">
        <h1 className="text-xl font-bold text-white leading-tight truncate max-w-lg">
          {title}
        </h1>

        <RiskBadge level={riskLevel} />
      </div>

      <p className="text-xs text-slate-300 mt-0.5">
        Analyzed on {date} · {reviewedCount} clauses reviewed
      </p>
    </div>
  )
}