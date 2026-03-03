import { Bell, Search } from 'lucide-react'

export function DashboardHeader() {
  return (
    <header className="sticky top-0 z-20 flex items-center justify-between px-8 py-4
      bg-white/70 backdrop-blur-xl border-b border-black/5"
    >
      <div>
        <h1 className="text-xl font-bold text-slate-900">
          Welcome back, Muhammad
        </h1>
        <p className="text-xs text-slate-500 mt-0.5">
          Contract intelligence — updated just now
        </p>
      </div>

      <div className="flex items-center gap-3">

        <button className="relative w-9 h-9 flex items-center justify-center rounded-xl
          text-slate-500 hover:bg-slate-100 transition-colors"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-white" />
        </button>

        <button className="w-9 h-9 flex items-center justify-center rounded-xl
          text-slate-500 hover:bg-slate-100 transition-colors"
        >
          <Search className="w-4 h-4" />
        </button>
      </div>
    </header>
  )
}