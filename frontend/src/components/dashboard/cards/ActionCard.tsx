import { motion } from 'framer-motion'
import type { LucideIcon } from 'lucide-react'
import { ArrowUpRight } from 'lucide-react'
import { Link } from 'react-router-dom'

const MotionLink = motion(Link)

type Props = {
  title: string
  description: string
  icon: LucideIcon
  to?: string
  variant?: 'primary' | 'secondary'
  delay?: number
}

export function ActionCard({
  title,
  description,
  icon: Icon,
  to = '#',
  variant = 'secondary',
  delay = 0,
}: Props) {
  const isPrimary = variant === 'primary'

  return (
    <MotionLink
      to={to}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.03,
        delay,
        ease: 'easeOut',
      }}
      whileHover={{ y: -4 }}
      className={`
        relative overflow-hidden p-6 rounded-2xl group transition-all duration-300
        ${isPrimary
          ? 'text-white bg-gradient-to-br from-[#1a1f2e] to-[#2d3550] shadow-xl'
          : 'bg-white/80 backdrop-blur border border-black/5 hover:shadow-lg'
        }
      `}
    >
      <div className="flex items-center justify-between mb-5">
        <div
          className={`
            w-10 h-10 flex items-center justify-center rounded-xl bg-none
          `}
        >
          <Icon
            className={`w-5 h-5 ${
              isPrimary ? 'text-white' : 'text-slate-700'
            }`}
          />
        </div>

        <ArrowUpRight
          className={`w-4 h-4 transition-opacity ${
            isPrimary ? 'opacity-70 text-white' : 'text-slate-300'
          } group-hover:opacity-100`}
        />
      </div>

      <h3
        className={`text-lg font-bold mb-1 ${
          isPrimary ? 'text-white' : 'text-slate-900'
        }`}
      >
        {title}
      </h3>

      <p
        className={`text-sm ${
          isPrimary ? 'text-white/70' : 'text-slate-500'
        }`}
      >
        {description}
      </p>
    </MotionLink>
  )
}