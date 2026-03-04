export function CompletedTodayCard() {
  return (
    <div className="rounded-2xl p-6 bg-gradient-to-br from-brand-900 to-brand-700 text-white shadow-soft">
      <h3 className="text-sm font-bold mb-1">
        Contracts Analyzed
      </h3>

      <div className="text-4xl font-bold mt-3 mb-5">
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