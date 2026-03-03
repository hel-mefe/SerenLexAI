import type { SeverityLevel } from './analysis'

export type ClauseId = string

export interface ClauseItem {
  id: ClauseId
  title: string
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