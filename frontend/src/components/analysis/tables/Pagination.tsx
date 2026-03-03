type Props = {
  page: number
  onChange: (page: number) => void
}

export function Pagination({
  page,
  onChange,
}: Props) {
  return (
    <div className="flex items-center justify-center gap-2 mt-8">
      <button
        disabled={page === 1}
        onClick={() => onChange(page - 1)}
        className="w-9 h-9 rounded-lg text-slate-400 disabled:opacity-50"
      >
        ‹
      </button>

      <button className="w-9 h-9 rounded-lg bg-slate-900 text-white shadow-lg">
        {page}
      </button>

      <button
        onClick={() => onChange(page + 1)}
        className="w-9 h-9 rounded-lg text-slate-700 hover:bg-white/80"
      >
        ›
      </button>
    </div>
  )
}