import { Sidebar } from '@/components/dashboard/sidebar/Sidebar'
import { Outlet } from 'react-router-dom'

export function DashboardLayout() {
  return (
    <div className="min-h-screen flex bg-dashboard-gradient">
      <Sidebar />

      <div className="flex-1 flex flex-col min-w-0">

        <main className="flex-1 p-8 overflow-auto space-y-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
}