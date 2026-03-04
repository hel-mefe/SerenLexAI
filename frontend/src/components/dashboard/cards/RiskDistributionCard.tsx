import { AlertTriangle, AlertCircle, ShieldCheck } from 'lucide-react'
import { useAnalysesList } from '@/api/analysis/hooks'

export function RiskDistributionCard() {
  const { data, isLoading, isError } = useAnalysesList({
    page: 1,
    pageSize: 100,
  })

  const items = data?.items ?? []

  const highCount = items.filter((item) => item.risk === 'High').length
  const mediumCount = items.filter((item) => item.risk === 'Medium').length
  const lowCount = items.filter((item) => item.risk === 'Low').length

  const total = highCount + mediumCount + lowCount

  if (isLoading) {
    return (
      <div className="rounded-2xl p-6 bg-white/80 backdrop-blur border border-black/5">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-bold text-slate-900">
            Risk Overview
          </h2>
        </div>

        <div className="flex items-center justify-center py-8">
          <div className="w-8 h-8 rounded-full border-2 border-slate-300 border-t-transparent animate-spin" />
        </div>
      </div>
    )
  }

  if (isError || !total) {
    return (
      <div className="rounded-2xl p-6 bg-white/80 backdrop-blur border border-black/5">
        <div className="flex items-center justify-between mb-1">
          <h2 className="text-base font-bold text-slate-900">
            Risk Overview
          </h2>
        </div>
        <p className="text-xs text-slate-400 mt-3">
          No risk data available yet. Run an analysis to see aggregated risk
          levels.
        </p>
      </div>
    )
  }

  return (
    <div className="rounded-2xl p-6 bg-white/80 backdrop-blur border border-black/5">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h2 className="text-base font-bold text-slate-900">
            Risk Overview
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Aggregated across your recent analyses
          </p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <RiskLevelCard
          tone="high"
          label="High Risk"
          count={highCount}
          total={total}
          icon={AlertTriangle}
          description="Analyses flagged as high risk"
        />
        <RiskLevelCard
          tone="medium"
          label="Medium Risk"
          count={mediumCount}
          total={total}
          icon={AlertCircle}
          description="Analyses requiring attention"
        />
        <RiskLevelCard
          tone="low"
          label="Low Risk"
          count={lowCount}
          total={total}
          icon={ShieldCheck}
          description="Analyses with low exposure"
        />
      </div>
    </div>
  )
}

type Tone = 'high' | 'medium' | 'low'

type RiskLevelCardProps = {
  tone: Tone
  label: string
  count: number
  total: number
  description: string
  icon: React.ComponentType<React.SVGProps<SVGSVGElement>>
}

function RiskLevelCard({
  tone,
  label,
  count,
  total,
  description,
  icon: Icon,
}: RiskLevelCardProps) {
  const percent = total ? Math.round((count / total) * 100) : 0

  const toneStyles: Record<
    Tone,
    {
      bg: string
      border: string
      text: string
      chipBg: string
      chipText: string
    }
  > = {
    high: {
      bg: 'bg-red-50',
      border: 'border-red-100',
      text: 'text-red-600',
      chipBg: 'bg-red-100',
      chipText: 'text-red-600',
    },
    medium: {
      bg: 'bg-amber-50',
      border: 'border-amber-100',
      text: 'text-amber-600',
      chipBg: 'bg-amber-100',
      chipText: 'text-amber-600',
    },
    low: {
      bg: 'bg-emerald-50',
      border: 'border-emerald-100',
      text: 'text-emerald-600',
      chipBg: 'bg-emerald-100',
      chipText: 'text-emerald-600',
    },
  }

  const styles = toneStyles[tone]

  return (
    <div
      className={`rounded-2xl p-4 ${styles.bg} border ${styles.border} flex flex-col gap-3`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div
            className={`w-8 h-8 rounded-xl flex items-center justify-center bg-white/80 ${styles.text}`}
          >
            <Icon className="w-4 h-4" />
          </div>
          <span className={`text-xs font-semibold uppercase ${styles.text}`}>
            {label}
          </span>
        </div>

        <span
          className={`px-2 py-0.5 rounded-full text-[11px] font-semibold ${styles.chipBg} ${styles.chipText}`}
        >
          {percent}%
        </span>
      </div>

      <div className="flex items-baseline gap-2">
        <span className={`text-3xl font-bold ${styles.text}`}>{count}</span>
        <span className="text-xs text-slate-500">analyses</span>
      </div>

      <p className="text-xs text-slate-500 leading-snug">{description}</p>
    </div>
  )
}