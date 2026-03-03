import { Link } from 'react-router-dom'
import { Plus } from 'lucide-react'

type Props = {
  total: number
}

export function AnalysesHeader({ total }: Props) {
  return (
    <header className="sticky top-0 z-20 flex items-center justify-between px-8 py-4 bg-white/70 backdrop-blur-xl border-b border-black/5 rounded-2xl mx-8">
      <div>
        <h1 className="text-xl font-bold text-slate-900">
          All Analyses
        </h1>
        <p className="text-xs text-slate-500 mt-0.5">
          {total} contracts analyzed
        </p>
      </div>

      <Link
        to="/upload"
        className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold text-white bg-gradient-to-br from-[#1a1f2e] to-[#2d3550] hover:shadow-lg transition-all"
      >
        <Plus className="w-4 h-4" />
        New Analysis
      </Link>
    </header>
  )
}