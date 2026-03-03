import { UploadCloud } from 'lucide-react'

type Props = {
  file: File | null
  onFileSelect: (file: File) => void
}

export function UploadDropzone({
  file,
  onFileSelect,
}: Props) {
  return (
    <div className="rounded-2xl p-12 text-center mb-6 bg-white/75 border-2 border-dashed border-black/10 backdrop-blur transition-all hover:border-black/20">
      <div className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-5 bg-slate-100">
        <UploadCloud className="w-8 h-8 text-slate-400" />
      </div>

      <h3 className="text-lg font-bold text-slate-900 mb-2">
        {file ? file.name : 'Drop your contract here'}
      </h3>

      <p className="text-sm text-slate-500 mb-6">
        PDF files up to 20 pages · Encrypted in transit
      </p>

      <label>
        <input
          type="file"
          accept=".pdf,.doc,.docx,.txt"
          className="hidden"
          onChange={(e) => {
            if (e.target.files?.[0]) {
              onFileSelect(e.target.files[0])
            }
          }}
        />
        <span className="inline-block px-6 py-2.5 rounded-xl text-sm font-semibold text-white cursor-pointer bg-gradient-to-br from-[#1a1f2e] to-[#2d3550] hover:opacity-90 transition-opacity">
          Browse Files
        </span>
      </label>
    </div>
  )
}