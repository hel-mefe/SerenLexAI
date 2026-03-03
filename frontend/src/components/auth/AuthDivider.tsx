export function AuthDivider({
  label = 'or continue with',
}: {
  label?: string
}) {
  return (
    <div className="flex items-center gap-3 my-6">
      <div className="flex-1 h-px bg-neutral-200" />
      <span className="text-xs text-neutral-400 whitespace-nowrap">
        {label}
      </span>
      <div className="flex-1 h-px bg-neutral-200" />
    </div>
  )
}