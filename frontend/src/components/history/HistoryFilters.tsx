type Props = {
  filter: string
  onChange: (value: any) => void
}

export function HistoryFilters({
  filter,
  onChange,
}: Props) {
  const options = ['All', 'UPLOAD', 'COMPLETED', 'FAILED']

  return (
    <div className="flex items-center gap-2">
      {options.map((option) => (
        <button
          key={option}
          onClick={() => onChange(option)}
          className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
            filter === option
              ? 'bg-slate-900 text-white shadow-lg'
              : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
          }`}
        >
          {option}
        </button>
      ))}
    </div>
  )
}