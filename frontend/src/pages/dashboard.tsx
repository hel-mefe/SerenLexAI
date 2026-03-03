import { Sidebar } from '@/components/dashboard/sidebar/Sidebar'
import { ActionCard } from '@/components/dashboard/cards/ActionCard'
import { RiskDistributionCard } from '@/components/dashboard/cards/RiskDistributionCard'
import { CompletedTodayCard } from '@/components/dashboard/cards/CompletedTodayCard'
import { motion } from 'framer-motion'

import {
  UploadCloud,
  Brain,
  FileChartColumn,
} from 'lucide-react'
import { RecentAnalysesCard } from '@/components/dashboard/cards/RecentAnalysesCard'
import { OptimizeCard } from '@/components/dashboard/cards/OptimizeCard'
import { ThisMonthCard } from '@/components/dashboard/cards/ThisMonthCard'

export function DashboardPage() {
  return (
    <div className="min-h-screen flex bg-dashboard-gradient">
      <Sidebar />

      <div className="flex-1 flex flex-col min-w-0">
        {/* <DashboardHeader /> */}

        <main className="flex-1 p-8 overflow-auto space-y-8">
          {/* Action Cards */}
        <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        className="flex items-center ml-2 justify-between"
        >
        <div>
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
        Quick Actions
        </h2>

        <p className="text-sm text-slate-500 max-w-xl">
        Take a quick action to analyze, review, or export contract insights instantly.
        </p>

        </div>
        </motion.div>            
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
            <div className="col-span-2 flex flex-col gap-y-6">
              <RiskDistributionCard />
              <RecentAnalysesCard />
            </div>

            <div className='space-y-5'>
                <CompletedTodayCard />
                <OptimizeCard />
                <ThisMonthCard />
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}