import {
  UploadCloud,
  CheckCircle,
  AlertCircle,
} from 'lucide-react'
import type { HistoryEvent } from '@/types/history'

const iconMap = {
  UPLOAD: UploadCloud,
  COMPLETED: CheckCircle,
  FAILED: AlertCircle,
}

const colorMap = {
  UPLOAD: 'text-blue-500',
  COMPLETED: 'text-emerald-500',
  FAILED: 'text-red-500',
}

export function HistoryItem({
  item,
}: {
  item: HistoryEvent
}) {
  const Icon = iconMap[item.type]

  return (
    <div className="relative pl-6">
      <div className="absolute -left-3 top-1.5 w-6 h-6 flex items-center justify-center rounded-full bg-white border border-slate-200 shadow-sm">
        <Icon
          className={`w-3.5 h-3.5 ${colorMap[item.type]}`}
        />
      </div>

      <div className="rounded-2xl p-4 bg-white/80 backdrop-blur border border-black/5">
        <div className="flex items-center justify-between">
          <p className="text-sm font-semibold text-slate-900">
            {item.title}
          </p>
          <span className="text-xs text-slate-400">
            {item.date}
          </span>
        </div>

        <p className="text-xs text-slate-500 mt-1">
          {item.description}
        </p>
      </div>
    </div>
  )
}