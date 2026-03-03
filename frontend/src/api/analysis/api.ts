import { apiClient } from '@/api/client'
import type {
  AnalysisFilter,
  AnalysisId,
} from '@/types/analysis'
import type {
  AnalysisCreateDto,
  AnalysisDetailDto,
  AnalysisDetail,
  AnalysisListQuery,
  AnalysisListResponseDto,
} from './dtos'
import {
  mapAnalysisDetailDto,
  mapAnalysisListItemDto,
} from './dtos'

/**
 * Fetches a paginated list of analyses from the backend.
 *
 * @param query Optional list query parameters such as search term, risk filter
 * and pagination information.
 * @returns A promise that resolves to the mapped analyses list including
 * pagination metadata.
 */
export async function fetchAnalyses(
  query: AnalysisListQuery = {},
): Promise<{
  items: ReturnType<typeof mapAnalysisListItemDto>[]
  total: number
  page: number
  pageSize: number
}> {
  const params: Record<string, string | number | undefined> = {}

  if (query.search) {
    params['search'] = query.search
  }

  if (query.filter && query.filter !== 'All') {
    params['risk'] = query.filter as Exclude<AnalysisFilter, 'All'>
  }

  if (query.page != null) {
    params['page'] = query.page
  }

  if (query.pageSize != null) {
    params['page_size'] = query.pageSize
  }

  const { data } = await apiClient.get<AnalysisListResponseDto>(
    '/analyses',
    { params },
  )

  return {
    items: data.items.map(mapAnalysisListItemDto),
    total: data.total,
    page: data.page,
    pageSize: data.page_size,
  }
}

/**
 * Fetches a single analysis with its aggregated risk information.
 *
 * @param id Identifier of the analysis to retrieve.
 * @returns A promise that resolves to the mapped {@link AnalysisDetail}.
 */
export async function fetchAnalysisDetail(
  id: AnalysisId,
): Promise<AnalysisDetail> {
  const { data } = await apiClient.get<AnalysisDetailDto>(
    `/analyses/${id}`,
  )
  return mapAnalysisDetailDto(data)
}

/**
 * Creates a new analysis resource on the backend.
 *
 * @param payload Payload describing the source of the analysis such as title,
 * source type and optional raw text.
 * @returns A promise that resolves to the created {@link AnalysisDetail}.
 */
export async function createAnalysis(
  payload: AnalysisCreateDto,
): Promise<AnalysisDetail> {
  const { data } = await apiClient.post<AnalysisDetailDto>(
    '/analyses',
    payload,
  )
  return mapAnalysisDetailDto(data)
}

