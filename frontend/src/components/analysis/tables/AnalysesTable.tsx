import { AnalysesTableRow } from './AnalysesTableRow'
import { AnalysesEmptyState } from './AnalysesEmptyState'
import type { AnalysisItem } from '@/types/analysis'

type Props = {
  data: AnalysisItem[]
}

export function AnalysesTable({ data }: Props) {
  const isEmpty = data.length === 0

  return (
    <div className="rounded-2xl overflow-hidden bg-white/85 backdrop-blur border border-black/5">
      {isEmpty ? (
        <AnalysesEmptyState />
      ) : (
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-200">
              {[
                'Contract',
                'Date',
                'Risk',
                'Clauses',
                'Status',
                '',
              ].map((col) => (
                <th
                  key={col}
                  className="text-left px-6 py-4 text-xs font-bold text-slate-600 uppercase tracking-wide"
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {data.map((item) => (
              <AnalysesTableRow
                key={item.id}
                item={item}
              />
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}