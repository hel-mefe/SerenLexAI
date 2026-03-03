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
}

export const SIDEBAR_ITEMS: SidebarItem[] = [
  { icon: Home, path: '/dashboard', key: 'home' },
  { icon: FileText, path: '/dashboard/analyses', key: 'analyses' },
  { icon: UploadCloud, path: '/dashboard/upload', key: 'upload' },
  { icon: History, path: '/dashboard/history', key: 'history' },
]

export const SIDEBAR_BOTTOM_ITEMS: SidebarItem[] = [
  { icon: Settings, path: '/dashboard/settings', key: 'settings' },
  { icon: RefreshCcw, path: '/dashboard/refresh', key: 'refresh' },
]