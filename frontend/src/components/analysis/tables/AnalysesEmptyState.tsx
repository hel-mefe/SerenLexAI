import { Link } from 'react-router-dom'
import { FileSearch, Plus } from 'lucide-react'

export function AnalysesEmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-6 text-center">
      <FileSearch className="w-12 h-12 text-slate-300 mb-4" aria-hidden />
      <h3 className="text-base font-semibold text-slate-900">
        No analyses yet
      </h3>
      <p className="text-sm text-slate-500 mt-2 max-w-sm">
        Upload a contract to get started. We’ll analyze clauses, flag risks, and give you a plain-English report.
      </p>
      <Link
        to="/dashboard/analyses/new"
        className="mt-6 inline-flex items-center gap-2 rounded-xl bg-sidebar-gradient px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:opacity-90 transition-opacity"
      >
        <Plus className="w-4 h-4" />
        New Analysis
      </Link>
    </div>
  )
}
