import type { SeverityLevel } from '@/types/analysis'
import type { ClauseId, ClauseItem } from '@/types/clause'
import type {
  ApiCollectionResponse,
  DtoMapper,
} from '@/api/types'

export interface ClauseDto {
  id: string
  title: string
  severity: SeverityLevel
  original_text: string
  risk_explanation: string
  recommended_action: string
  clause_type: string | null
  position_index: number | null
}

export type ClauseListResponseDto =
  ApiCollectionResponse<ClauseDto>

export interface ClauseListQuery {
  analysisId: string
  severity?: SeverityLevel | 'All' | undefined
}

export const mapClauseDto: DtoMapper<ClauseDto, ClauseItem> = (dto) => {
  return {
    id: dto.id as ClauseId,
    title: dto.title,
    severity: dto.severity,
    originalText: dto.original_text,
    riskExplanation: dto.risk_explanation,
    recommendation: dto.recommended_action,
  }
}

