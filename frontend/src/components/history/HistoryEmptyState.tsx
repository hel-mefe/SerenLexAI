import { Clock } from 'lucide-react'

export function HistoryEmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <Clock className="w-10 h-10 text-slate-300 mb-4" />
      <h3 className="text-sm font-bold text-slate-900">
        No activity yet
      </h3>
      <p className="text-xs text-slate-500 mt-1">
        Your contract analysis history will appear here.
      </p>
    </div>
  )
}