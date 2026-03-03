import { NavLink } from 'react-router-dom'
import type { LucideIcon } from 'lucide-react'

type Props = {
  icon: LucideIcon
  path: string
}

export function SidebarItem({ icon: Icon, path }: Props) {
  return (
    <NavLink to={path}>
      {({ isActive }) => (
        <div
          className={`w-11 h-11 flex items-center justify-center rounded-xl transition-all duration-200
          ${
            isActive
              ? 'bg-gradient-to-br from-slate-700 to-slate-900 text-white shadow-lg'
              : 'text-slate-400 hover:bg-white/10 hover:text-white'
          }`}
        >
          <Icon size={18} />
        </div>
      )}
    </NavLink>
  )
}