import { DashboardLayout } from '@/components/layouts/DashboardLayout'
import { Sidebar } from '@/components/dashboard/sidebar/Sidebar'
import { DashboardHeader } from '@/components/dashboard/DashboardHeader'

export function DashboardPage() {
  return (
    <DashboardLayout>
      <Sidebar />

      <div className="flex-1 flex flex-col min-w-0">
        <DashboardHeader />

        <main className="flex-1 p-8 overflow-auto">
          {/* We will insert reusable cards here next */}
          <div className="text-slate-600">
            Dashboard content goes here...
          </div>
        </main>
      </div>
    </DashboardLayout>
  )
}