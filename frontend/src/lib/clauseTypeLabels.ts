/**
 * User-friendly labels for clause types.
 * Backend uses ClauseType enum (e.g. PAYMENT, INDEMNIFICATION); we display these labels in the UI.
 */
const CLAUSE_TYPE_LABELS: Record<string, string> = {
  definitions: 'Definitions',
  liability: 'Liability',
  termination: 'Termination',
  payment: 'Payment Terms',
  confidentiality: 'Confidentiality',
  indemnification: 'Indemnification',
  intellectual_property: 'Intellectual Property',
  governing_law: 'Governing Law',
  force_majeure: 'Force Majeure',
  other: 'Other',
}

function normaliseClauseTypeKey(raw: string | null | undefined): string | null {
  if (raw == null || typeof raw !== 'string') return null
  let s = raw.trim()
  if (s.startsWith('ClauseType.')) s = s.slice('ClauseType.'.length)
  return s.toLowerCase() || null
}

/**
 * Returns a user-friendly label for a clause type. Use for UI display only.
 * Falls back to the given title if the type is unknown (e.g. custom clauses).
 */
export function getClauseTypeDisplayLabel(
  clauseType: string | null | undefined,
  fallbackTitle: string
): string {
  const key = normaliseClauseTypeKey(clauseType ?? fallbackTitle)
  if (key && CLAUSE_TYPE_LABELS[key]) return CLAUSE_TYPE_LABELS[key]
  const fromTitle = fallbackTitle.trim()
  if (fromTitle) return fromTitle
  return 'Unnamed Clause'
}
