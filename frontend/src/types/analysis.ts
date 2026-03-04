export type SeverityLevel = 'High' | 'Medium' | 'Low'

export type RiskLevel = SeverityLevel

export type AnalysisStatus = 'pending' | 'completed' | 'failed'

export type AnalysisId = string

export interface AnalysisItem {
  id: AnalysisId
  name: string
  date: string
  time?: string
  risk: RiskLevel
  clauses: number
  score: number
  status: AnalysisStatus
}

export interface AnalysisScoreBreakdown {
  high: number
  medium: number
  low: number
}

export interface AnalysisSummary {
  id: AnalysisId
  title: string
  analyzedAt: string
  flaggedCount: number
  score: number
  overallRisk: RiskLevel
  breakdown: AnalysisScoreBreakdown
}

export type AnalysisFilter = 'All' | SeverityLevel