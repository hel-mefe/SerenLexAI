export type HistoryEventType =
  | 'UPLOAD'
  | 'COMPLETED'
  | 'FAILED'

export interface HistoryEvent {
  id: string
  type: HistoryEventType
  title: string
  description: string
  date: string
}

export const mockHistory: HistoryEvent[] = [
  {
    id: '1',
    type: 'UPLOAD',
    title: 'Contract Uploaded',
    description: 'Service Agreement — Acme Corp',
    date: 'Dec 18, 2024 · 14:12',
  },
  {
    id: '2',
    type: 'COMPLETED',
    title: 'Analysis Completed',
    description: '12 clauses flagged · High Risk',
    date: 'Dec 18, 2024 · 14:32',
  },
  {
    id: '3',
    type: 'FAILED',
    title: 'Analysis Failed',
    description: 'Parsing error detected',
    date: 'Dec 17, 2024 · 11:03',
  },
]