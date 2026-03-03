export function FormInput({
  label,
}: {
  label: string
}) {
  return (
    <div className="mb-4">
      <label className="block text-xs font-semibold text-neutral-500 uppercase mb-2">
        {label}
      </label>
      <input
        className="w-full px-4 py-3.5 rounded-xl bg-neutral-100 border border-border-light focus:ring-2 focus:ring-brand-600/20 outline-none transition"
      />
    </div>
  )
}