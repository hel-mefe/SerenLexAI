import type { SeverityLevel } from './analysis'

export type ClauseId = string

export interface ClauseItem {
  id: ClauseId
  title: string
  /** Raw clause type from API (e.g. "payment", "indemnification"); use for display via getClauseTypeDisplayLabel */
  clauseType?: string | null
  severity: SeverityLevel
  originalText: string
  riskExplanation: string
  recommendation: string
}

export interface ClauseNavigationItem {
  id: ClauseId
  title: string
  severity: SeverityLevel
}

export interface ClauseFilterState {
  severity: 'All' | SeverityLevel
}