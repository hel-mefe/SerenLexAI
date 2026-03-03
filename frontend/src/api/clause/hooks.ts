import { useQuery } from '@tanstack/react-query'

import type { SeverityLevel } from '@/types/analysis'
import { clausesKeys } from './keys'
import { fetchClausesForAnalysis } from './api'

export function useClausesByAnalysis(options: {
  analysisId: string | undefined
  severity?: SeverityLevel | 'All' | undefined
}) {
  const { analysisId, severity } = options

  return useQuery({
    queryKey: clausesKeys.byAnalysis(analysisId, severity),
    queryFn: () => {
      if (!analysisId) {
        throw new Error('analysisId is required')
      }

      return fetchClausesForAnalysis({
        analysisId,
        severity,
      })
    },
    enabled: Boolean(analysisId),
  })
}

