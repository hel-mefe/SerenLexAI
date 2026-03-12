import { Navigate } from 'react-router-dom'
import { authStorage } from '@/lib/auth.storage'

export function ProtectedRoute({
  children,
}: {
  children: React.ReactNode
}) {
  if (!authStorage.isAuthenticated()) {
    return <Navigate to="/signin" replace />
  }

  return <>{children}</>
}