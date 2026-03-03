import {
  Home,
  FileText,
  UploadCloud,
  History,
  Settings,
  RefreshCcw,
  type LucideIcon,
} from 'lucide-react'

export interface SidebarItem {
  icon: LucideIcon
  path: string
  key: string
  tooltip: string
}

export const SIDEBAR_ITEMS: SidebarItem[] = [
  { icon: Home, path: '/dashboard', key: 'home', tooltip: 'Home' },
  { icon: FileText, path: '/dashboard/analyses', key: 'analyses', tooltip: 'Analyses' },
  { icon: UploadCloud, path: '/dashboard/upload', key: 'upload', tooltip: 'Upload' },
  { icon: History, path: '/dashboard/history', key: 'history', tooltip: 'History' },
]

export const SIDEBAR_BOTTOM_ITEMS: SidebarItem[] = [
  { icon: Settings, path: '/dashboard/settings', key: 'settings', tooltip: 'Settings' },
  { icon: RefreshCcw, path: '/dashboard/refresh', key: 'refresh', tooltip: 'Sync' },
]