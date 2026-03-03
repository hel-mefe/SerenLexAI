export function BackgroundEffects() {
  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
      <div className="absolute -top-24 -left-24 w-[600px] h-[600px] bg-indigo-500/10 rounded-full blur-3xl" />
      <div className="absolute -bottom-24 -right-24 w-[500px] h-[500px] bg-emerald-500/10 rounded-full blur-3xl" />
    </div>
  )
}