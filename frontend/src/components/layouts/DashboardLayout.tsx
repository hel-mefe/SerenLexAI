type Props = {
  children: React.ReactNode
}

export function DashboardLayout({ children }: Props) {
  return (
    <div className="min-h-screen flex bg-gradient-to-br from-neutral-100 via-neutral-200 to-neutral-100">
      {children}
    </div>
  )
}