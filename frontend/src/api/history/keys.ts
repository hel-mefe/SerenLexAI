import type { HistoryEventType } from '@/types/history'

export const historyKeys = {
  all: ['history'] as const,

  list: (type: HistoryEventType | 'All' | undefined) =>
    [...historyKeys.all, 'list', type ?? 'All'] as const,
}

