import {
  Home,
  FileText,
  UploadCloud,
  History,
  type LucideIcon,
} from 'lucide-react'

export interface SidebarItemConfig {
  icon: LucideIcon
  path: string
  key: string
  tooltip: string
  /** When true, this item is only active for the exact path (e.g. /dashboard/analyses not /dashboard/analyses/new) */
  end?: boolean
}

export const SIDEBAR_ITEMS: SidebarItemConfig[] = [
  { icon: Home, path: '/dashboard', key: 'home', tooltip: 'Home', end: true },
  { icon: FileText, path: '/dashboard/analyses', key: 'analyses', tooltip: 'Analyses', end: true },
  { icon: UploadCloud, path: '/dashboard/analyses/new', key: 'Contract', tooltip: 'Contract', end: true },
  { icon: History, path: '/dashboard/history', key: 'history', tooltip: 'History' },
]

export const SIDEBAR_BOTTOM_ITEMS: SidebarItemConfig[] = []