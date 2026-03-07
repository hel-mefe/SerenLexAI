import { Download, Sparkles } from 'lucide-react'

export function ReportActions() {
  return (
    <div className="flex items-center justify-between rounded-2xl p-5 bg-white border border-black/5">
      <div className="flex items-center gap-2 text-sm text-slate-600">
        <Sparkles className="w-4 h-4 text-amber-500" />
        AI analysis
      </div>

      <button className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900 text-white text-sm font-semibold hover:bg-slate-800 transition">
        <Download className="w-4 h-4" />
        Export PDF
      </button>
    </div>
  )
}