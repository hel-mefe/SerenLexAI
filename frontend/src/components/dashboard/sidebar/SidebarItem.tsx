import { NavLink } from 'react-router-dom'
import type { LucideIcon } from 'lucide-react'
import { useState, useRef } from 'react'
import { AnimatePresence, motion } from 'framer-motion'

type Props = {
  icon: LucideIcon
  path: string
  label?: string
  end?: boolean
}

export function SidebarItem({ icon: Icon, path, label, end = false }: Props) {
  const [hovered, setHovered] = useState(false)
  const [coords, setCoords] = useState({ top: 0, left: 0 })
  const ref = useRef<HTMLDivElement>(null)

  const handleMouseEnter = () => {
    if (ref.current) {
      const rect = ref.current.getBoundingClientRect()
      setCoords({ top: rect.top + rect.height / 2, left: rect.right + 10 })
    }
    setHovered(true)
  }

  return (
    <div
      ref={ref}
      className="relative flex items-center"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={() => setHovered(false)}
    >
      <NavLink to={path} end={end}>
        {({ isActive }) => (
          <div
            className="w-11 h-11 flex items-center justify-center rounded-xl transition-all duration-200"
            style={{
              background: isActive
                ? 'linear-gradient(135deg, #1A1F2E 0%, #2D3550 100%)'
                : hovered
                ? 'linear-gradient(135deg, rgba(26,31,52,0.75) 0%, rgba(45,53,80,0.5) 100%)'
                : 'transparent',
              boxShadow: isActive
                ? '0 4px 16px rgba(13,17,23,0.5), inset 0 1px 0 rgba(255,255,255,0.07)'
                : hovered
                ? 'inset 0 1px 0 rgba(99,102,241,0.12), 0 0 16px rgba(26,31,52,0.5)'
                : 'none',
              color: isActive || hovered ? 'white' : '#94A3B8',
              border: hovered && !isActive
                ? '1px solid rgba(45,53,80,0.6)'
                : '1px solid transparent',
            }}
          >
            <Icon size={18} />
          </div>
        )}
      </NavLink>

      <AnimatePresence>
        {hovered && (
          <motion.div
            initial={{ opacity: 0, x: -6, scale: 0.95 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, x: -4, scale: 0.95 }}
            transition={{ duration: 0.15, ease: 'easeOut' }}
            className="pointer-events-none z-[9999]"
            style={{ position: 'fixed', top: coords.top, left: coords.left, transform: 'translateY(-50%)' }}
          >
            <div
              className="relative flex items-center px-3 py-1.5 rounded-lg backdrop-blur-xl border border-white/[0.04]"
              style={{
                background: 'linear-gradient(135deg, rgba(8,10,18,0.97) 0%, rgba(12,15,28,0.95) 50%, rgba(10,14,26,0.97) 100%)',
                boxShadow: '0 8px 32px rgba(0,0,0,0.7), 0 1px 0 rgba(255,255,255,0.03) inset, 0 -1px 0 rgba(0,0,0,0.4) inset',
              }}
            >
              <div
                className="absolute inset-x-0 top-0 h-px rounded-full"
                style={{ background: 'linear-gradient(90deg, transparent, rgba(99,102,241,0.2), transparent)' }}
              />
              <div
                className="absolute inset-x-0 bottom-0 h-px rounded-full"
                style={{ background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent)' }}
              />
              <span className="text-[11px] font-medium tracking-wide text-slate-300/80 whitespace-nowrap capitalize">
                {label}
              </span>
            </div>
            <div className="absolute top-1/2 -translate-y-1/2 -left-[5px] w-0 h-0 border-t-[5px] border-t-transparent border-b-[5px] border-b-transparent border-r-[5px] border-r-[rgba(8,10,18,0.97)]" />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}