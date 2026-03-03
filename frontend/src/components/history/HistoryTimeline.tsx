import { motion } from 'framer-motion'
import { HistoryItem } from './HistoryItem'
import type { HistoryEvent } from '@/types/history'

export function HistoryTimeline({
  items,
}: {
  items: HistoryEvent[]
}) {
  return (
    <div className="relative border-l border-slate-200 ml-3 space-y-6">
      {items.map((item, index) => (
        <motion.div
          key={item.id}
          initial={{ opacity: 0, x: -8 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.05 }}
        >
          <HistoryItem item={item} />
        </motion.div>
      ))}
    </div>
  )
}