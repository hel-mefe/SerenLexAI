export function PublicLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <div className="w-screen h-screen">{children}</div>
}