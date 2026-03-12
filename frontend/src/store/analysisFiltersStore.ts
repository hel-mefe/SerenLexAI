import { create } from 'zustand'

import type {
  AnalysisStatus,
  SeverityLevel,
} from '@/types/analysis'

export type SeverityFilterValue = 'All' | SeverityLevel
export type StatusFilterValue = 'All' | AnalysisStatus

interface AnalysisFiltersState {
  search: string
  severity: SeverityFilterValue
  status: StatusFilterValue
  page: number
  setSearch: (value: string) => void
  setSeverity: (value: SeverityFilterValue) => void
  setStatus: (value: StatusFilterValue) => void
  setPage: (value: number) => void
  reset: () => void
}

const initialState: Pick<
  AnalysisFiltersState,
  'search' | 'severity' | 'status' | 'page'
> = {
  search: '',
  severity: 'All',
  status: 'All',
  page: 1,
}

export const useAnalysisFiltersStore =
  create<AnalysisFiltersState>((set) => ({
    ...initialState,
    setSearch: (value) => set({ search: value, page: 1 }),
    setSeverity: (value) => set({ severity: value, page: 1 }),
    setStatus: (value) => set({ status: value }),
    setPage: (value) => set({ page: value }),
    reset: () => set(initialState),
  }))

