import { SIDEBAR_ITEMS, SIDEBAR_BOTTOM_ITEMS } from '@/config/sidebar.config'
import { SidebarItem } from './SidebarItem'
import { NavLink } from 'react-router-dom'

export function Sidebar() {
  return (
    <aside className="w-20 flex-shrink-0 flex flex-col items-center py-6 gap-2 sticky top-0 h-screen z-30 bg-sidebar-gradient border-r border-white/5">
      
      {/* Logo */}
      <div className="w-11 h-11 flex items-center justify-center mb-4">
        <h2 className='text-white'>SLAI</h2>
      </div>

      <div className="w-8 h-px bg-white/10 mb-2" />

      {/* Main Nav */}
      <nav className="flex flex-col items-center gap-4 flex-1">
        {SIDEBAR_ITEMS.map((item) => (
          <NavLink
            key={item.key}
            to={item.path}
            end={item.path === '/dashboard'} 
            className={({ isActive }) =>
              `
              relative w-11 h-11 flex items-center justify-center rounded-xl transition-all duration-200
              ${
                isActive
                  ? 'bg-gradient-to-br from-slate-700 to-slate-900 shadow-lg text-white'
                  : 'text-slate-400 hover:bg-white/10 hover:text-white'
              }
              `
            }
          >
            <item.icon className="w-5 h-5" />
          </NavLink>
        ))}
      </nav>
  
      {/* Bottom Section */}
      <div className="flex flex-col items-center gap-2 mt-auto">
        <div className="w-8 h-px bg-white/10 mb-2" />

        {SIDEBAR_BOTTOM_ITEMS.map((item: any) => (
          <SidebarItem
            key={item.key}
            icon={item.icon}
            path={item.path}
          />
        ))}

        {/* User Avatar */}
        <div className="w-11 h-11 mt-3 rounded-xl bg-gradient-to-br from-slate-600 to-slate-800 flex items-center justify-center text-white text-sm font-bold border border-white/10">
          HE
        </div>
      </div>
    </aside>
  )
}