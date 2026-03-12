import type { AnalysisFilter, AnalysisId } from '@/types/analysis'

export const analysesKeys = {
  all: ['analyses'] as const,

  list: (params?: {
    search?: string | undefined
    filter?: AnalysisFilter | undefined
    page?: number | undefined
    pageSize?: number | undefined
  }) =>
    [
      ...analysesKeys.all,
      'list',
      params?.search ?? '',
      params?.filter ?? 'All',
      params?.page ?? 1,
      params?.pageSize ?? 10,
    ] as const,

  detail: (id: AnalysisId | undefined) =>
    [...analysesKeys.all, 'detail', id] as const,
}

