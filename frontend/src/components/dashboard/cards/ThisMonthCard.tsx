import { motion } from 'framer-motion'

export function ThisMonthCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.6 }}
      className="rounded-2xl p-6 bg-white/80 backdrop-blur border border-black/5"
    >
      <h3 className="text-sm font-bold text-slate-900 mb-4">
        This Month
      </h3>

      <div className="space-y-3.5">
        <StatRow label="Total Contracts" value="342" />
        <StatRow label="Avg. Analysis Time" value="1.8 min" />
        <StatRow label="Risks Identified" value="1,247" />
        <StatRow label="Time Saved" value="68 hrs" highlight />
      </div>
    </motion.div>
  )
}

function StatRow({
  label,
  value,
  highlight,
}: {
  label: string
  value: string
  highlight?: boolean
}) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-xs text-slate-500">{label}</span>
      <span
        className={`text-sm font-bold ${
          highlight ? 'text-emerald-600' : 'text-slate-900'
        }`}
      >
        {value}
      </span>
    </div>
  )
}