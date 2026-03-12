import { useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { isAxiosError } from 'axios'

import { NewAnalysisHeader } from '@/components/newanalysis/NewAnalysisHeader'
import { UploadDropzone } from '@/components/newanalysis/UploadDropZone'
import { StartAnalysisButton } from '@/components/newanalysis/StartAnalysisButton'
import { FeatureHighlights } from '@/components/newanalysis/FeatureHighlights'
import { useCreateAnalysisFromFile } from '@/api/analysis/hooks'
import toast from 'react-hot-toast'
import { toastAnalysisQueued } from '@/lib/toast'
import { useNewAnalysisStore } from '@/store/newAnalysisStore'

function getErrorMessage(error: unknown): string {
  if (isAxiosError(error) && error.response?.data?.detail) {
    const d = error.response.data.detail
    return typeof d === 'string' ? d : Array.isArray(d) ? d.map((x: { msg?: string }) => x.msg).filter(Boolean).join(' ') : 'Something went wrong.'
  }
  return error instanceof Error ? error.message : 'Something went wrong. Please try again.'
}

export function NewAnalysisPage() {
  const navigate = useNavigate()
  const { title, file, setTitle, setFile, reset } = useNewAnalysisStore()

  const createUpload = useCreateAnalysisFromFile()

  const canAnalyze = useMemo(() => !!file, [file])

  const isSubmitting = createUpload.isPending
  const error = createUpload.error
  const errorMessage = error ? getErrorMessage(error) : null

  const handleSubmit = async () => {
    if (!canAnalyze || isSubmitting || !file) return
    const displayTitle = title.trim() || file.name || 'New analysis'
    try {
      const result = await createUpload.mutateAsync({
        file,
        title: displayTitle,
      })
      toastAnalysisQueued(displayTitle)
      reset()
      navigate(`/dashboard/analyses/${result.id}`)
    } catch (err) {
      toast.error(getErrorMessage(err))
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="flex-1 flex flex-col min-w-0"
    >
      <NewAnalysisHeader />

      <main className="flex-1 p-8 overflow-auto">
        <div className="max-w-3xl mx-auto">
          <div className="mb-4">
            <label className="block text-sm font-semibold text-slate-700 mb-1.5">
              Title (optional)
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder={file ? file.name : 'e.g. Service Agreement — Acme Corp'}
              className="w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-300"
            />
          </div>

          <UploadDropzone
            file={file}
            onFileSelect={setFile}
          />

          {errorMessage && (
            <div className="mb-4 rounded-xl border border-red-200 bg-red-50/80 px-4 py-3 text-sm text-red-700">
              {errorMessage}
            </div>
          )}

          <StartAnalysisButton
            disabled={!canAnalyze}
            loading={isSubmitting}
            onClick={handleSubmit}
          />

          <FeatureHighlights />
        </div>
      </main>
    </motion.div>
  )
}