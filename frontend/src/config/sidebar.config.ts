import {
  Home,
  FileText,
  UploadCloud,
  History,
  Calendar,
  Settings,
  RefreshCcw,
} from 'lucide-react'

export const SIDEBAR_ITEMS = [
  { icon: Home, path: '/dashboard', key: 'home' },
  { icon: FileText, path: '/analyses', key: 'analyses' },
  { icon: UploadCloud, path: '/upload', key: 'upload' },
  { icon: History, path: '/history', key: 'history' },
  { icon: Calendar, path: '/calendar', key: 'calendar' },
]

export const SIDEBAR_BOTTOM_ITEMS = [
  { icon: Settings, path: '/settings', key: 'settings' },
  { icon: RefreshCcw, path: '/refresh', key: 'refresh' },
]