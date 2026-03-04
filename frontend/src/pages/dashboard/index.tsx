import { ActionCard } from '@/components/dashboard/cards/ActionCard'
import { RiskDistributionCard } from '@/components/dashboard/cards/RiskDistributionCard'
import { CompletedTodayCard } from '@/components/dashboard/cards/CompletedTodayCard'
import { RecentAnalysesCard } from '@/components/dashboard/cards/RecentAnalysesCard'
import { OptimizeCard } from '@/components/dashboard/cards/OptimizeCard'
import { motion } from 'framer-motion'

import {
  UploadCloud,
  FileText,
  History,
} from 'lucide-react'

export function DashboardPage() {
  return (
    <>
      {/* Quick Actions Header */}
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        className="ml-2"
      >
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
          Quick Actions
        </h2>

        <p className="text-sm text-slate-500 max-w-xl mt-1">
          Take a quick action to analyze, review, or export contract insights instantly.
        </p>
      </motion.div>

      {/* Action Cards */}
      <div className="grid grid-cols-3 gap-5">
        <ActionCard
          title="Analyze Contract"
          description="Upload PDF or paste text"
          icon={UploadCloud}
          variant="primary"
          delay={0}
        />

        <ActionCard
          title="View Analyses"
          description="See all completed and in-progress analyses"
          icon={FileText}
          to="/dashboard/analyses"
          delay={0.1}
        />

        <ActionCard
          title="Activity History"
          description="Review uploads, analyses, and system actions"
          icon={History}
          to="/dashboard/history"
          delay={0.2}
        />
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2 flex flex-col gap-y-6">
          <RiskDistributionCard />
          <RecentAnalysesCard />
        </div>

        <div className="space-y-5">
          <CompletedTodayCard />
          <OptimizeCard />
        </div>
      </div>
    </>
  )
}