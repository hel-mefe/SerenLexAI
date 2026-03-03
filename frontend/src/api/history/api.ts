import { apiClient } from '@/api/client'
import type { HistoryEventType } from '@/types/history'
import type { ActionsListResponseDto } from './dtos'
import { mapActionDtoToHistoryEvent } from './dtos'

/**
 * Fetches the event-sourced history stream from the backend.
 *
 * @param params.type Optional filter for history event type; when omitted or
 * set to `"All"` all event types are returned.
 * @returns A promise that resolves to the mapped history events and total
 * count.
 */
export async function fetchHistoryEvents(params?: {
  type?: HistoryEventType | 'All' | undefined
}) {
  const { type } = params ?? {}

  const query: Record<string, string | undefined> = {}
  if (type && type !== 'All') {
    query['type'] = type
  }

  const { data } = await apiClient.get<ActionsListResponseDto>(
    '/actions',
    { params: query },
  )

  return {
    items: data.items.map(mapActionDtoToHistoryEvent),
    total: data.total,
  }
}

