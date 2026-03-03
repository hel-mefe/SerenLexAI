export function CompletedTodayCard() {
  return (
    <div className="rounded-2xl p-6 bg-white/80 backdrop-blur border border-black/5">
      <div className="flex items-center justify-between mb-1">
        <h3 className="text-sm font-bold text-slate-900">
          Completed Today
        </h3>
        <span className="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full">
          +10%
        </span>
      </div>

      <div className="text-4xl font-bold text-slate-900 mt-3 mb-5">
        46
      </div>

      <div className="flex items-end gap-1 h-16">
        {[40,55,45,70,60,80,65,75,85,70,90,95].map((h,i)=>(
          <div
            key={i}
            className="flex-1 rounded-t bg-gradient-to-t from-[#1a1f2e] to-slate-500"
            style={{ height: `${h}%` }}
          />
        ))}
      </div>
    </div>
  )
}