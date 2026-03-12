import React from 'react'
import { BackgroundEffects } from './BackgroundEffects'

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="h-full w-full flex items-center justify-center p-6 bg-brand-950 hero-grid-bg relative overflow-hidden">
      <BackgroundEffects />
      {children}
    </div>
  )
}