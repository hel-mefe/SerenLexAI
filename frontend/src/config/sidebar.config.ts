import {
  Home,
  FileText,
  UploadCloud,
  History,
  Calendar,
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
  { icon: FileText, path: '/analyses', key: 'analyses' },
  { icon: UploadCloud, path: '/upload', key: 'upload' },
  { icon: History, path: '/history', key: 'history' },
]

export const SIDEBAR_BOTTOM_ITEMS: SidebarItem[] = [
  { icon: Settings, path: '/settings', key: 'settings' },
  { icon: RefreshCcw, path: '/refresh', key: 'refresh' },
]