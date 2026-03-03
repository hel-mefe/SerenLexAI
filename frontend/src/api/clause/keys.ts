import type { SeverityLevel } from '@/types/analysis'

export const clausesKeys = {
  all: ['clauses'] as const,

  byAnalysis: (
    analysisId: string | undefined,
    severity: SeverityLevel | 'All' | undefined,
  ) =>
    [
      ...clausesKeys.all,
      'byAnalysis',
      analysisId ?? '',
      severity ?? 'All',
    ] as const,
}

