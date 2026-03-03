import { FileText } from 'lucide-react'

type Props = {
  value: string
  onChange: (value: string) => void
}

export function PasteTextInput({
  value,
  onChange,
}: Props) {
  return (
    <div className="rounded-2xl p-8 mb-6 bg-white/75 border border-black/5 backdrop-blur">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 flex items-center justify-center rounded-xl bg-slate-100">
          <FileText className="w-5 h-5 text-slate-700" />
        </div>

        <div>
          <h3 className="text-lg font-bold text-slate-900">
            Paste Contract Text
          </h3>
          <p className="text-xs text-slate-500">
            Minimum 200 characters recommended
          </p>
        </div>
      </div>

      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Paste your contract text here..."
        className="w-full min-h-[220px] rounded-xl text-sm bg-slate-50 border border-slate-200 p-4 focus:outline-none focus:ring-2 focus:ring-slate-300 transition-all resize-none"
      />
    </div>
  )
}