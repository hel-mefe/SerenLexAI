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
 * Creates a new analysis from pasted text.
 *
 * @param payload Payload with title, source_type 'paste', and raw_text.
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

/**
 * Creates a new analysis from an uploaded PDF (max 20 pages).
 *
 * @param file PDF file to upload.
 * @param title Optional title; defaults to file name.
 * @returns A promise that resolves to the created {@link AnalysisDetail}.
 * @throws Axios error with 400 if document exceeds 20 pages or invalid type,
 * 413 if file too large, 422 if extraction fails.
 */
export async function createAnalysisFromFile(
  file: File,
  title: string,
): Promise<AnalysisDetail> {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('title', title || file.name || 'Uploaded document')

  const { data } = await apiClient.post<AnalysisDetailDto>(
    '/analyses/upload',
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    },
  )
  return mapAnalysisDetailDto(data)
}

/**
 * Downloads the uploaded source PDF for an analysis (upload-based only).
 * Triggers a file download in the browser.
 *
 * @param id Analysis ID.
 * @param suggestedFilename Optional filename (e.g. original_filename or title + .pdf).
 * @throws Axios error with 404 if no PDF is available.
 */
export async function downloadAnalysisPdf(
  id: string,
  suggestedFilename?: string,
): Promise<void> {
  const { data } = await apiClient.get<Blob>(`/analyses/${id}/pdf`, {
    responseType: 'blob',
  })
  const name = (suggestedFilename || id).replace(/\.pdf$/i, '') + '.pdf'
  const url = URL.createObjectURL(data)
  const a = document.createElement('a')
  a.href = url
  a.download = name
  a.click()
  URL.revokeObjectURL(url)
}

/**
 * Downloads the generated SerenLexAI risk report PDF for an analysis.
 * Filename will be {base}_serenlexai_report.pdf.
 *
 * @param id Analysis ID.
 * @param suggestedBaseName Optional base name (e.g. original_filename or title, without .pdf).
 * @throws Axios error with 404 if report is not available.
 */
export async function downloadAnalysisReportPdf(
  id: string,
  suggestedBaseName?: string,
): Promise<void> {
  const { data } = await apiClient.get<Blob>(`/analyses/${id}/report/pdf`, {
    responseType: 'blob',
  })
  const base = (suggestedBaseName || id).replace(/\.pdf$/i, '').trim() || id
  const safeBase = base.replace(/[^\w\s.-]/g, '_').replace(/\s+/g, '_').slice(0, 200)
  const name = `${safeBase}_serenlexai_report.pdf`
  const url = URL.createObjectURL(data)
  const a = document.createElement('a')
  a.href = url
  a.download = name
  a.click()
  URL.revokeObjectURL(url)
}

