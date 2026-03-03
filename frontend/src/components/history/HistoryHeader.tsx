export function HistoryHeader() {
  return (
    <header className="sticky top-0 z-20 rounded-3xl bg-auth-gradient flex items-center justify-between px-8 py-4 bg-white/70 backdrop-blur-xl border-b border-black/5">
      <div>
        <h1 className="text-xl font-bold text-white">
          Activity History
        </h1>
        <p className="text-xs text-slate-300 mt-0.5">
          Track uploads, analyses, and system events
        </p>
      </div>
    </header>
  )
}