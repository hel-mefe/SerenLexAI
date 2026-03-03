import { motion } from 'framer-motion'

type Props = {
  analysisId?: string
}

export function ReportHeader({ analysisId }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="flex items-center justify-between"
    >
      <div>
        <h1 className="text-2xl font-bold text-slate-900">
          Analysis Report #{analysisId ?? '—'}
        </h1>

        <p className="text-sm text-slate-500 mt-1">
          AI contract risk assessment · Generated just now
        </p>
      </div>
    </motion.div>
  )
}