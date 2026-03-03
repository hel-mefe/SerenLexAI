type Props = {
  label: string
  placeholder?: string
  field: any
}

export function FormInput({
  label,
  placeholder,
  field,
}: Props) {
  return (
    <div className="mb-4">
      <label className="block text-xs font-semibold text-neutral-500 uppercase tracking-wider mb-2">
        {label}
      </label>

      <input
        value={field.state.value}
        onChange={(e) => field.handleChange(e.target.value)}
        onBlur={field.handleBlur}
        placeholder={placeholder}
        className="w-full px-4 py-3.5 rounded-xl text-sm text-slate-800 placeholder-slate-300 outline-none transition-all"
        style={{
          background: 'rgb(247, 248, 250)',
          border: '1.5px solid rgb(234, 236, 240)',
        }}
      />

      {field.state.meta.errors?.length ? (
        <p className="text-xs text-risk-high mt-2">
          {field.state.meta.errors[0]}
        </p>
      ) : null}
    </div>
  )
}