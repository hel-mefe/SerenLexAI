import { Routes, Route, Navigate } from 'react-router-dom'
import { PublicLayout } from './PublicLayout'
import { ProtectedRoute } from './ProtectedRoute'

import SignInPage from '@/pages/SignInPage'

import { DashboardLayout } from '@/components/layouts/DashboardLayout.tsx'
import { DashboardPage } from '@/pages/dashboard'
import { AnalysesPage } from '@/pages/dashboard/Analyses'
import { HistoryPage } from '@/pages/dashboard/HistoryPage'
import { AnalysisReportPage } from '@/pages/dashboard/Analyses/AnalysisReportPage'
import { NewAnalysisPage } from '@/pages/dashboard/Analyses/New'

export function AppRouter() {
  return (
    <Routes>
      {/* Public */}
      <Route
        path="/"
        element={
          <PublicLayout>
            <SignInPage />
          </PublicLayout>
        }
      />

      {/* Protected Dashboard */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }
      >
        {/* Default Dashboard Home */}
        <Route index element={<DashboardPage />} />

        <Route path="analyses" element={<AnalysesPage />} />
        <Route path="history" element={<HistoryPage />} />
        <Route path="analyses/:analysisId" element={<AnalysisReportPage />} />
        <Route path="analyses/new" element={<NewAnalysisPage />} />
      </Route>

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}