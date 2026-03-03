import { Outlet } from 'react-router-dom'

export function DashboardLayout() {
  return (
    <div className="min-h-screen bg-surface flex">
      {/* Sidebar will go here later */}
      <div className="flex-1 p-8">
        <Outlet />
      </div>
    </div>
  )
}