import type {
  AnalysisFilter,
  AnalysisId,
  AnalysisItem,
  SeverityLevel,
} from '@/types/analysis'
import type {
  ApiPaginatedResponse,
  DtoMapper,
} from '@/api/types'

/**
 * DTOs reflect the raw JSON contract of the backend.
 * They intentionally mirror snake_case naming coming from FastAPI / Pydantic.
 */

export interface AnalysisListItemDto {
  id: string
  name: string
  date: string
  risk: SeverityLevel | null
  clauses: number
  score: number
  status: string
}

export type AnalysisListResponseDto =
  ApiPaginatedResponse<AnalysisListItemDto>

export interface AnalysisDetailDto {
  id: string
  title: string
  original_filename: string | null
  source_type: string
  status: string
  overall_risk: SeverityLevel | null
  risk_score: number | null
  flagged_count: number
  high_count: number
  medium_count: number
  low_count: number
  created_at: string
  updated_at: string
}

export interface AnalysisCreateDto {
  title: string
  original_filename?: string | null
  source_type: 'upload' | 'paste'
  raw_text?: string | null
}

export interface AnalysisListQuery {
  search?: string | undefined
  filter?: AnalysisFilter | undefined
  page?: number | undefined
  pageSize?: number | undefined
}

/**
 * Mapping helpers from backend DTOs to frontend domain types.
 */

export const mapAnalysisListItemDto: DtoMapper<
  AnalysisListItemDto,
  AnalysisItem
> = (dto) => {
  const dateObj = new Date(dto.date)

  const date = dateObj.toLocaleDateString('en-US', {
    month: 'short',
    day: '2-digit',
    year: 'numeric',
  })

  const time = dateObj.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
  })

  const rawStatus = dto.status ?? 'pending'
  const status =
    rawStatus === 'completed'
      ? 'completed'
      : rawStatus === 'failed'
        ? 'failed'
        : 'pending'

  return {
    id: dto.id as AnalysisId,
    name: dto.name,
    date,
    time,
    risk: dto.risk ?? 'Low',
    clauses: dto.clauses,
    score: dto.score,
    status,
  }
}

export interface AnalysisDetail {
  id: AnalysisId
  title: string
  originalFilename: string | null
  sourceType: string
  status: string
  overallRisk: SeverityLevel | null
  score: number | null
  flaggedCount: number
  high: number
  medium: number
  low: number
  createdAt: Date
  updatedAt: Date
}

export const mapAnalysisDetailDto: DtoMapper<
  AnalysisDetailDto,
  AnalysisDetail
> = (dto) => {
  return {
    id: dto.id as AnalysisId,
    title: dto.title,
    originalFilename: dto.original_filename,
    sourceType: dto.source_type,
    status: dto.status,
    overallRisk: dto.overall_risk,
    score: dto.risk_score,
    flaggedCount: dto.flagged_count,
    high: dto.high_count,
    medium: dto.medium_count,
    low: dto.low_count,
    createdAt: new Date(dto.created_at),
    updatedAt: new Date(dto.updated_at),
  }
}

