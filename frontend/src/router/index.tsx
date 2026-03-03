import { Routes, Route, Navigate } from 'react-router-dom'
import { PublicLayout } from './PublicLayout'
import { ProtectedRoute } from './ProtectedRoute'
import SignInPage from '@/pages/signin'
import { DashboardPage } from '@/pages/dashboard'

// import OverviewPage from '@/pages/dashboard/OverviewPage'

export function AppRouter() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route
        path="/"
        element={
          <PublicLayout>
            <SignInPage />
          </PublicLayout>
        }
      />

      {/* Protected Routes */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      >

      </Route>

      {/* Fallback */}
      <Route
        path="*"
        element={<Navigate to="/" replace />}
      />
    </Routes>
  )
}