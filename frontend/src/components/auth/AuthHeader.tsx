export function AuthHeader() {
  return (
    <div className="flex items-center justify-end px-10 pt-8">
      <span className="text-sm text-neutral-400 mr-2">
        New here?
      </span>
      <button
        type="button"
        className="text-sm font-semibold text-neutral-900 hover:text-neutral-700 transition-colors"
      >
        Request Access
      </button>
    </div>
  )
}