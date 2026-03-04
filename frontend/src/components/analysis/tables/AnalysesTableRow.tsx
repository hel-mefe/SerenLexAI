import { useNavigate } from 'react-router-dom'
import { RiskBadge } from '@/components/analysis/badges/RiskBadge'
import type { AnalysisItem } from '@/types/analysis'

type Props = {
  item: AnalysisItem
}

export function AnalysesTableRow({ item }: Props) {
  const navigate = useNavigate()

  const isReady = item.status === 'completed'

  const handleRowClick = () => {
    if (!isReady) return
    navigate(`/dashboard/analyses/${item.id}`)
  }

  return (
    <tr
      onClick={handleRowClick}
      className={`border-b border-slate-100 transition-colors group ${
        isReady
          ? 'hover:bg-slate-50 cursor-pointer'
          : 'opacity-80 cursor-not-allowed'
      }`}
    >
      <td className="px-6 py-4 text-sm font-semibold text-slate-900">
        {item.name}
      </td>

      <td className="px-6 py-4 text-sm text-slate-600">
        {item.date}
      </td>

      <td className="px-6 py-4">
        {isReady ? (
          <RiskBadge level={item.risk} />
        ) : (
          <span className="text-xs font-medium text-slate-400">
            N/A
          </span>
        )}
      </td>

      <td className="px-6 py-4 text-sm font-medium">
        {isReady ? item.clauses : 'N/A'}
      </td>

      <td className="px-6 py-4 text-sm font-bold">
        {isReady ? item.score : 'N/A'}
      </td>

      <td className="px-6 py-4">
        {isReady ? (
          <span className="inline-flex items-center rounded-full border border-emerald-200 bg-emerald-50/80 px-2.5 py-0.5 text-[11px] font-semibold text-emerald-700">
            Done
          </span>
        ) : item.status === 'failed' ? (
          <span className="inline-flex items-center rounded-full border border-red-200 bg-red-50/80 px-2.5 py-0.5 text-[11px] font-semibold text-red-700">
            Failed
          </span>
        ) : (
          <span className="inline-flex items-center rounded-full border border-amber-200 bg-amber-50/80 px-2.5 py-0.5 text-[11px] font-semibold text-amber-700">
            Processing…
          </span>
        )}
      </td>

      <td className="px-6 py-4 text-right">
        {isReady ? (
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation()
              navigate(`/dashboard/analyses/${item.id}`)
            }}
            className="px-4 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 opacity-0 group-hover:opacity-100 transition-all cursor-pointer"
          >
            View
          </button>
        ) : (
          <span className="text-[11px] font-medium text-slate-400">
            Preparing…
          </span>
        )}
      </td>
    </tr>
  )
}