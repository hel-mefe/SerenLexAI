import { Routes, Route, Navigate } from 'react-router-dom'
import { PublicLayout } from './PublicLayout'
import { ProtectedRoute } from './ProtectedRoute'

import SignInPage from '@/pages/SignInPage'

import { DashboardLayout } from '@/components/layouts/DashboardLayout.tsx'
import { DashboardPage } from '@/pages/dashboard'
import { AnalysesPage } from '@/pages/dashboard/Analyses'
import { UploadPage } from '@/pages/dashboard/UploadPage'
import { HistoryPage } from '@/pages/dashboard/HistoryPage'
import { SettingsPage } from '@/pages/dashboard/SettingsPage'
import { RefreshPage } from '@/pages/dashboard/RefreshPage'
import { AnalysisReportPage } from '@/pages/dashboard/Analyses/AnalysisReportPage'

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
        <Route path="upload" element={<UploadPage />} />
        <Route path="history" element={<HistoryPage />} />
        <Route path="settings" element={<SettingsPage />} />
        <Route path="refresh" element={<RefreshPage />} />
        <Route path="analyses/:analysisId" element={<AnalysisReportPage />} />
      </Route>

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}