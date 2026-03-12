type Props = {
  page: number
  totalPages: number
  onChange: (page: number) => void
}

export function Pagination({
  page,
  totalPages,
  onChange,
}: Props) {
  const isFirst = page <= 1
  const isLast = page >= totalPages

  return (
    <div className="flex items-center justify-center gap-2 mt-8">
      <button
        disabled={isFirst}
        onClick={() => !isFirst && onChange(page - 1)}
        className="w-9 h-9 rounded-lg text-slate-400 disabled:opacity-50"
      >
        ‹
      </button>

      <button className="w-9 h-9 rounded-lg bg-slate-900 text-white shadow-lg">
        {page}
      </button>

      <button
        disabled={isLast}
        onClick={() => !isLast && onChange(page + 1)}
        className="w-9 h-9 rounded-lg text-slate-700 hover:bg-white/80 disabled:opacity-50"
      >
        ›
      </button>
    </div>
  )
}