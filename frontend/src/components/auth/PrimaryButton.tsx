export function PrimaryButton({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <button className="w-full py-3.5 rounded-xl text-white font-semibold bg-card-gradient hover:opacity-90 transition shadow-soft">
      {children}
    </button>
  )
}