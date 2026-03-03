import { motion } from 'framer-motion'
import { FileText, PlayCircle } from 'lucide-react'
import { SeverityBadge } from '../badges/SeverityBadge'
import { Link } from 'react-router-dom'

type Analysis = {
  title: string
  date: string
  flagged: number
  severity: 'High' | 'Medium' | 'Low'
}

const mockData: Analysis[] = [
  {
    title: 'Service Agreement — Acme Corp',
    date: 'Dec 18, 2024',
    flagged: 12,
    severity: 'High',
  },
  {
    title: 'Software License — TechStart Ltd',
    date: 'Dec 17, 2024',
    flagged: 8,
    severity: 'Medium',
  },
  {
    title: 'Consulting Contract — BuildCo',
    date: 'Dec 15, 2024',
    flagged: 5,
    severity: 'Low',
  },
]

export function RecentAnalysesCard() {
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

        <Link to='/dashboard/analyses' className='cursor-pointer'>
            <button className="text-xs cursor-pointer font-semibold text-slate-500 hover:text-slate-800 transition-colors">
            See all →
            </button>
        </Link>
      </div>

      <div className="space-y-2">
        {mockData.map((item, index) => (
          <div
            key={index}
            className="flex items-center justify-between px-4 py-3.5 rounded-xl border border-black/5 hover:bg-slate-50 transition group"
          >
            <div className="flex items-center gap-3 flex-1 min-w-0">
              <div className="w-9 h-9 flex items-center justify-center rounded-xl bg-slate-100">
                <FileText className="w-4 h-4 text-slate-500" />
              </div>

              <div className="min-w-0">
                <p className="text-sm font-semibold text-slate-900 truncate">
                  {item.title}
                </p>
                <p className="text-xs text-slate-400 mt-0.5">
                  {item.date} · {item.flagged} clauses flagged
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3 ml-4">
              <SeverityBadge severity={item.severity} />

              <button className="opacity-0 group-hover:opacity-100 transition">
                <PlayCircle className="w-4 h-4 text-slate-500 hover:text-slate-800" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  )
}