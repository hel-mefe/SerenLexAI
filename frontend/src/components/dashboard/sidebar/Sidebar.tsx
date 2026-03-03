import { SIDEBAR_ITEMS, SIDEBAR_BOTTOM_ITEMS } from '@/config/sidebar.config'
import { SidebarItem } from './SidebarItem'
import LogoIcon from '@/assets/logo.png'

export function Sidebar() {
  return (
    <aside className="w-20 flex-shrink-0 flex flex-col items-center py-6 gap-2 sticky top-0 h-screen z-30 bg-sidebar-gradient border-r border-white/5">
      
      {/* Logo */}
      <div className="w-11 h-11 flex items-center justify-center mb-4">
        <h2 className='text-white'>SLAI</h2>
      </div>

      <div className="w-8 h-px bg-white/10 mb-2" />

      {/* Main Nav */}
      <nav className="flex flex-col items-center gap-2 flex-1">
        {SIDEBAR_ITEMS.map((item: any) => (
          <SidebarItem
            key={item.key}
            icon={item.icon}
            path={item.path}
          />
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