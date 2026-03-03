import { useNavigate } from 'react-router-dom'
import { RiskBadge } from '@/components/analysis/badges/RiskBadge'
import type { AnalysisItem } from '@/types/analysis'
import { Link } from 'react-router-dom'

type Props = {
  item: AnalysisItem
}

export function AnalysesTableRow({ item }: Props) {
  const navigate = useNavigate()

  return (
    <tr
      onClick={() =>
        navigate(`/dashboard/analyses/${item.id}`)
      }
      className="border-b border-slate-100 hover:bg-slate-50 transition-colors group cursor-pointer"
    >
      <td className="px-6 py-4 text-sm font-semibold text-slate-900">
        {item.name}
      </td>

      <td className="px-6 py-4 text-sm text-slate-600">
        {item.date}
      </td>

      <td className="px-6 py-4">
        <RiskBadge level={item.risk} />
      </td>

      <td className="px-6 py-4 text-sm font-medium">
        {item.clauses}
      </td>

      <td className="px-6 py-4 text-sm font-bold">
        {item.score}
      </td>

      <td className="px-6 py-4 text-right">
        <Link className='cursor-pointer' to='/dashboard/analyses/1'>
            <button className="px-4 py-1.5 cursor-pointer rounded-lg text-xs font-semibold bg-slate-100 opacity-0 group-hover:opacity-100 transition-all">
            View
            </button>
        </Link>
      </td>
    </tr>
  )
}