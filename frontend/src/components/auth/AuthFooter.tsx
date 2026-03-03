export function AuthFooter() {
  return (
    <div className="flex items-center justify-between px-10 pb-8 text-xs text-neutral-400">
      <span>© {new Date().getFullYear()} SerenLexAI Inc.</span>

      <div className="flex items-center gap-4">
        <button className="hover:text-neutral-600 transition-colors">
          Privacy
        </button>
        <button className="hover:text-neutral-600 transition-colors">
          Terms
        </button>
        <button className="hover:text-neutral-600 transition-colors">
          Contact
        </button>
      </div>
    </div>
  )
}