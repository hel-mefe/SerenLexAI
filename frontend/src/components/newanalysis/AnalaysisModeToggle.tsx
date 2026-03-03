import { FileUp, Type } from 'lucide-react'

type Props = {
  mode: 'upload' | 'paste'
  onChange: (mode: 'upload' | 'paste') => void
}

export function AnalysisModeToggle({
  mode,
  onChange,
}: Props) {
  return (
    <div className="flex items-center gap-2 p-1 rounded-2xl mb-8 w-fit bg-white/85 border border-black/5">
      <button
        onClick={() => onChange('upload')}
        className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all ${
          mode === 'upload'
            ? 'text-white shadow-md bg-gradient-to-br from-[#1a1f2e] to-[#2d3550]'
            : 'text-slate-500 hover:text-slate-700'
        }`}
      >
        <FileUp className="w-4 h-4" />
        Upload PDF
      </button>

      <button
        onClick={() => onChange('paste')}
        className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all ${
          mode === 'paste'
            ? 'text-white shadow-md bg-gradient-to-br from-[#1a1f2e] to-[#2d3550]'
            : 'text-slate-500 hover:text-slate-700'
        }`}
      >
        <Type className="w-4 h-4" />
        Paste Text
      </button>
    </div>
  )
}