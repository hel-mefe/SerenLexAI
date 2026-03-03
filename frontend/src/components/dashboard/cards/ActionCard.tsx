import type { LucideIcon } from 'lucide-react'
import { ArrowUpRight } from 'lucide-react'
import { Link } from 'react-router-dom'

type Props = {
  title: string
  description: string
  icon: LucideIcon
  to?: string
  variant?: 'primary' | 'secondary'
}

export function ActionCard({
  title,
  description,
  icon: Icon,
  to = '#',
  variant = 'secondary',
}: Props) {
  const isPrimary = variant === 'primary'

  return (
    <Link
      to={to}
      className={`
        relative overflow-hidden p-6 rounded-2xl group transition-all
        hover:-translate-y-1
        ${isPrimary
          ? 'text-white bg-gradient-to-br from-[#1a1f2e] to-[#2d3550] shadow-xl'
          : 'bg-white/80 backdrop-blur border border-black/5 hover:shadow-lg'
        }
      `}
    >
      <div className="flex items-center justify-between mb-5">
        <div
          className={`
            w-10 h-10 flex items-center justify-center rounded-xl
            ${isPrimary ? 'bg-white/10' : 'bg-slate-100'}
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
    </Link>
  )
}