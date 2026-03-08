import toast from 'react-hot-toast'
import { FileSearch } from 'lucide-react'

/**
 * Show a branded toast when a contract has been submitted for analysis.
 * Call after redirecting the user to the analyses list.
 *
 * @param title Optional contract title to include in the message.
 */
export function toastAnalysisQueued(title?: string) {
  const message = title
    ? `"${title}" is being analyzed. We'll have your risk report ready shortly.`
    : 'Your contract is being analyzed. We\'ll have your risk report ready shortly.'

  toast.success(message, {
    duration: 5500,
    icon: <FileSearch className="w-5 h-5 shrink-0" aria-hidden />,
  })
}
