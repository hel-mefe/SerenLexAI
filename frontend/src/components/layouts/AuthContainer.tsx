export function AuthContainer({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="relative z-10 flex w-full max-w-[1020px] min-h-[620px] rounded-4xl shadow-glow overflow-hidden bg-none">
      {children}
    </div>
  )
}