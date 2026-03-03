import { Sidebar } from '@/components/dashboard/sidebar/Sidebar'
import { DashboardHeader } from '@/components/dashboard/DashboardHeader'
import { ActionCard } from '@/components/dashboard/cards/ActionCard'
import { RiskDistributionCard } from '@/components/dashboard/cards/RiskDistributionCard'
import { CompletedTodayCard } from '@/components/dashboard/cards/CompletedTodayCard'

import {
  UploadCloud,
  Brain,
  FileChartColumn,
} from 'lucide-react'

export function DashboardPage() {
  return (
    <div className="min-h-screen flex bg-dashboard-gradient">
      <Sidebar />

      <div className="flex-1 flex flex-col min-w-0">
        <DashboardHeader />

        <main className="flex-1 p-8 overflow-auto space-y-8">
          {/* Action Cards */}
            <div className="grid grid-cols-3 gap-5 relative z-0">
            <ActionCard
                title="Analyze Contract"
                description="Upload PDF or paste text"
                icon={UploadCloud}
                variant="primary"
                delay={0}
            />

            <ActionCard
                title="Risk Analyzer"
                description="Detailed clause breakdown"
                icon={Brain}
                delay={0.1}
            />

            <ActionCard
                title="Export Report"
                description="Generate PDF summaries"
                icon={FileChartColumn}
                delay={0.2}
            />
            </div>

          {/* Content Grid */}
          <div className="grid grid-cols-3 gap-6">
            <div className="col-span-2">
              <RiskDistributionCard />
            </div>

            <CompletedTodayCard />
          </div>
        </main>
      </div>
    </div>
  )
}