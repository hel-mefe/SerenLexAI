import { apiClient } from '@/api/client'
import type { SeverityLevel } from '@/types/analysis'
import type { ClauseListResponseDto } from './dtos'
import { mapClauseDto } from './dtos'

/**
 * Fetches clauses associated with a single analysis.
 *
 * @param params.analysisId Identifier of the analysis to retrieve clauses for.
 * @param params.severity Optional severity filter; when omitted or set to
 * `"All"` all severities are returned.
 * @returns A promise that resolves to the mapped clause list and total count.
 */
export async function fetchClausesForAnalysis(params: {
  analysisId: string
  severity?: SeverityLevel | 'All' | undefined
}) {
  const { analysisId, severity } = params

  const query: Record<string, string | undefined> = {}
  if (severity && severity !== 'All') {
    query['severity'] = severity
  }

  const { data } = await apiClient.get<ClauseListResponseDto>(
    `/analyses/${analysisId}/clauses`,
    { params: query },
  )

  return {
    items: data.items.map(mapClauseDto),
    total: data.total,
  }
}

