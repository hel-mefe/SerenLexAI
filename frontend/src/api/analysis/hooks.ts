import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

import type {
  AnalysisFilter,
  AnalysisId,
} from '@/types/analysis'
import type { AnalysisCreateDto, AnalysisDetail } from './dtos'
import { analysesKeys } from './keys'
import { historyKeys } from '@/api/history/keys'
import {
  createAnalysis,
  createAnalysisFromFile,
  fetchAnalyses,
  fetchAnalysisDetail,
} from './api'

export function useAnalysesList(options?: {
  search?: string | undefined
  filter?: AnalysisFilter | undefined
  page?: number | undefined
  pageSize?: number | undefined
}) {
  const { search, filter, page, pageSize } = options ?? {}

  return useQuery({
    queryKey: analysesKeys.list({ search, filter }),
    queryFn: () =>
      fetchAnalyses({
        search,
        filter,
        page,
        pageSize,
      }),
  })
}

export function useAnalysisDetail(
  id: AnalysisId | undefined,
  options?: { refetchIntervalMs?: number },
) {
  const refetchIntervalMs = options?.refetchIntervalMs

  return useQuery<AnalysisDetail, Error>({
    queryKey: analysesKeys.detail(id),
    queryFn: () => {
      if (!id) {
        throw new Error('Analysis id is required')
      }
      return fetchAnalysisDetail(id)
    },
    enabled: Boolean(id),
    refetchInterval: refetchIntervalMs,
  })
}

export function useCreateAnalysis() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (payload: AnalysisCreateDto) => createAnalysis(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: analysesKeys.all })
      queryClient.invalidateQueries({ queryKey: historyKeys.all })
    },
  })
}

export function useCreateAnalysisFromFile() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ file, title }: { file: File; title: string }) =>
      createAnalysisFromFile(file, title),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: analysesKeys.all })
      queryClient.invalidateQueries({ queryKey: historyKeys.all })
    },
  })
}

