import { Link } from 'react-router-dom'
import { ArrowLeft, Plus } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

type Props = {
  total: number
}

export function AnalysesHeader({ total }: Props) {
  const navigate = useNavigate()

  return (
    <header className="sticky top-0 z-20 rounded-3xl bg-auth-gradient flex items-center justify-between px-8 py-4 backdrop-blur-xl border-b border-black/5 mx-8">
      <div className="flex items-center gap-4">
        <button
          onClick={() => navigate(-1)}
          className="w-9 h-9 flex items-center justify-center rounded-xl text-white/70 hover:bg-white/10 hover:text-white transition-all"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>

        <div>
          <h1 className="text-xl font-bold text-white">
            All Analyses
          </h1>
          <p className="text-xs text-slate-300 mt-0.5">
            {total} contracts analyzed
          </p>
        </div>
      </div>

      <Link
        to="/dashboard/analyses/new"
        className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold text-white bg-gradient-to-br from-[#1a1f2e] to-[#2d3550] hover:shadow-lg transition-all border border-white/10"
      >
        <Plus className="w-4 h-4" />
        New Analysis
      </Link>
    </header>
  )
}