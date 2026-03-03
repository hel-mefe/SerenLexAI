import { useQuery } from '@tanstack/react-query'

import type { HistoryEventType } from '@/types/history'
import { historyKeys } from './keys'
import { fetchHistoryEvents } from './api'

export function useHistoryEvents(options?: {
  type?: HistoryEventType | 'All' | undefined
}) {
  const type = options?.type

  return useQuery({
    queryKey: historyKeys.list(type),
    queryFn: () => fetchHistoryEvents({ type }),
  })
}

