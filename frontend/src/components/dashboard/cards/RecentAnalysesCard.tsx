import { motion } from 'framer-motion'
import { FileText, PlayCircle } from 'lucide-react'
import { Link } from 'react-router-dom'

import { SeverityBadge } from '../badges/SeverityBadge'
import { useAnalysesList } from '@/api/analysis/hooks'
import type { AnalysisItem } from '@/types/analysis'

export function RecentAnalysesCard() {
  const { data, isLoading, isError } = useAnalysesList({
    page: 1,
    pageSize: 3,
  })

  const items = (data?.items ?? []).slice(0, 3)

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.4 }}
      className="rounded-2xl p-6 bg-white/80 backdrop-blur border border-black/5 hover:shadow-xl transition-shadow"
    >
      <div className="flex items-center justify-between mb-5">
        <h2 className="text-base font-bold text-slate-900">
          Recent Analyses
        </h2>

        <Link
          to="/dashboard/analyses"
          className="cursor-pointer"
        >
          <button className="text-xs cursor-pointer font-semibold text-slate-500 hover:text-slate-800 transition-colors">
            See all →
          </button>
        </Link>
      </div>

      {isLoading ? (
        <div className="flex flex-col items-center justify-center py-8 text-center">
          <div className="w-8 h-8 rounded-full border-2 border-slate-300 border-t-transparent animate-spin" />
          <p className="mt-3 text-xs text-slate-500">
            Loading recent analyses…
          </p>
        </div>
      ) : isError || items.length === 0 ? (
        <p className="text-xs text-slate-400">
          No recent analyses available yet.
        </p>
      ) : (
        <div className="space-y-2">
          {items.map((item: AnalysisItem) => (
            <div
              key={item.id}
              className="flex items-center justify-between px-4 py-3.5 rounded-xl border border-black/5 hover:bg-slate-50 transition group"
            >
              <div className="flex items-center gap-3 flex-1 min-w-0">
                <div className="w-9 h-9 flex items-center justify-center rounded-xl bg-slate-100">
                  <FileText className="w-4 h-4 text-slate-500" />
                </div>

                <div className="min-w-0">
                  <p className="text-sm font-semibold text-slate-900 truncate">
                    {item.name}
                  </p>
                  <p className="text-xs text-slate-400 mt-0.5">
                    {item.date}
                    {item.time ? ` · ${item.time}` : ''} · {item.clauses} clauses
                    flagged
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-3 ml-4">
                <SeverityBadge severity={item.risk} />

                <button className="opacity-0 group-hover:opacity-100 transition">
                  <PlayCircle className="w-4 h-4 text-slate-500 hover:text-slate-800" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </motion.div>
  )
}