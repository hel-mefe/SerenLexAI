import { SIDEBAR_ITEMS, SIDEBAR_BOTTOM_ITEMS } from '@/config/sidebar.config'
import { SidebarItem } from './SidebarItem'
import { LogOut, ShieldCheck } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'


export function Sidebar() {
  const { logout } = useAuth()

  return (
  <aside className="w-22 flex-shrink-0 flex flex-col items-center py-6 gap-2 sticky top-0 h-screen z-30 bg-sidebar-gradient border-r border-white/5 relative after:absolute after:top-[10%] after:bottom-[10%] after:right-0 after:w-px after:bg-gradient-to-b after:from-transparent after:via-white/15 after:to-transparent after:pointer-events-none">      {/* Logo */}
      <div className="w-11 h-11 mb-4 relative flex items-center justify-center">
        <div className="absolute inset-0 rounded-2xl bg-logo-gradient shadow-lg shadow-gray-800/40 border border-auth-gradient/60" />
        <div className="relative flex items-center justify-center gap-1.5 text-white">
          <ShieldCheck className="w-6 h-6 text-auth-gradient" />
        </div>
      </div>

      <div className="w-8 h-px bg-white/10 mb-2" />

      {/* Main Nav */}
      <nav className="flex flex-col items-center gap-4 flex-1">
        {SIDEBAR_ITEMS.map((item) => (
          <SidebarItem
            key={item.key}
            icon={item.icon}
            path={item.path}
            label={item.tooltip}
            end={item.path === '/dashboard'}
          />
        ))}
      </nav>

      {/* Bottom Section */}
      <div className="flex flex-col items-center gap-2 mt-auto">
        <div className="w-8 h-px bg-white/10 mb-2" />

        {SIDEBAR_BOTTOM_ITEMS.map((item) => (
          <SidebarItem
            key={item.key}
            icon={item.icon}
            path={item.path}
            label={item.tooltip}
          />
        ))}

        <SidebarItem
          icon={LogOut}
          path="#"
          label="log out"
          onClick={logout}
        />

        {/* User Avatar */}
        <div className="w-11 h-11 mt-3 rounded-xl bg-gradient-to-br from-slate-600 to-slate-800 flex items-center justify-center text-white text-sm font-bold border border-white/10">
          MU
        </div>
      </div>
    </aside>
  )
}