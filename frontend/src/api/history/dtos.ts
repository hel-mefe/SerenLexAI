import type {
  HistoryEvent,
  HistoryEventType,
} from '@/types/history'
import type {
  ApiCollectionResponse,
  DtoMapper,
} from '@/api/types'

export interface ActionDto {
  id: string
  type: HistoryEventType
  title: string
  description: string
  created_at: string
  analysis_id: string | null
  user_id: string | null
}

export type ActionsListResponseDto =
  ApiCollectionResponse<ActionDto>

export interface HistoryListQuery {
  type?: HistoryEventType | 'All' | undefined
}

export const mapActionDtoToHistoryEvent: DtoMapper<
  ActionDto,
  HistoryEvent
> = (dto) => {
  const createdAt = new Date(dto.created_at)

  const date = createdAt.toLocaleString('en-US', {
    month: 'short',
    day: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })

  return {
    id: dto.id,
    type: dto.type,
    title: dto.title,
    description: dto.description,
    date,
  }
}

