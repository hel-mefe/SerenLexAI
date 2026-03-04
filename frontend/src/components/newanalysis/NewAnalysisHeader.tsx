import { ArrowLeft } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export function NewAnalysisHeader() {
  const navigate = useNavigate()

  return (
    <header className="sticky top-0 z-20 rounded-3xl bg-auth-gradient flex items-center justify-between px-8 py-4 backdrop-blur-xl border-b border-black/5">
      <div className="flex items-center gap-3">
        <button
          onClick={() => navigate('/dashboard')}
          className="w-9 h-9 flex items-center justify-center rounded-xl text-white/70 hover:bg-white/10 hover:text-white transition-all"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>

        <div>
          <h1 className="text-xl font-bold text-white">
            New Analysis
          </h1>
          <p className="text-xs text-slate-300 mt-0.5">
            Upload a contract to get started
          </p>
        </div>
      </div>
    </header>
  )
}