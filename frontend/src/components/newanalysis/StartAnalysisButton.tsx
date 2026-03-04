import { Loader2, Radar } from 'lucide-react'

type Props = {
  disabled: boolean
  loading?: boolean
  onClick?: () => void
}

export function StartAnalysisButton({
  disabled,
  loading = false,
  onClick,
}: Props) {
  const isDisabled = disabled || loading

  return (
    <button
      type="button"
      disabled={isDisabled}
      onClick={onClick}
      className={`w-full py-4 rounded-2xl text-base font-bold transition-all flex items-center justify-center gap-2 ${
        isDisabled
          ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
          : 'bg-gradient-to-br from-[#1a1f2e] to-[#2d3550] text-white hover:shadow-lg'
      }`}
    >
      {loading ? (
        <>
          <Loader2 className="w-5 h-5 animate-spin" />
          Analyzing…
        </>
      ) : (
        <>
          <Radar className="w-5 h-5" />
          Start Risk Analysis
        </>
      )}
    </button>
  )
}