import { Radar } from 'lucide-react'

export function StartAnalysisButton({
  disabled,
}: {
  disabled: boolean
}) {
  return (
    <button
      disabled={disabled}
      className={`w-full py-4 rounded-2xl text-base font-bold transition-all ${
        disabled
          ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
          : 'bg-gradient-to-br from-[#1a1f2e] to-[#2d3550] text-white hover:shadow-lg'
      }`}
    >
      <Radar className="inline mr-2 w-4 h-4" />
      Start Risk Analysis
    </button>
  )
}