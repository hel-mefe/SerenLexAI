import { useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { isAxiosError } from 'axios'

import { NewAnalysisHeader } from '@/components/newanalysis/NewAnalysisHeader'
import { AnalysisModeToggle } from '@/components/newanalysis/AnalaysisModeToggle'
import { UploadDropzone } from '@/components/newanalysis/UploadDropZone'
import { StartAnalysisButton } from '@/components/newanalysis/StartAnalysisButton'
import { PasteTextInput } from '@/components/newanalysis/PasteTextInput'
import { FeatureHighlights } from '@/components/newanalysis/FeatureHighlights'
import { useCreateAnalysis, useCreateAnalysisFromFile } from '@/api/analysis/hooks'
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
  const {
    mode,
    title,
    file,
    text,
    setMode,
    setTitle,
    setFile,
    setText,
    reset,
  } = useNewAnalysisStore()

  const createPaste = useCreateAnalysis()
  const createUpload = useCreateAnalysisFromFile()

  const canAnalyze = useMemo(() => {
    if (mode === 'upload') return !!file
    return text.trim().length > 50
  }, [mode, file, text])

  const isSubmitting = createPaste.isPending || createUpload.isPending
  const error = createPaste.error ?? createUpload.error
  const errorMessage = error ? getErrorMessage(error) : null

  const handleSubmit = async () => {
    if (!canAnalyze || isSubmitting) return
    const displayTitle = title.trim() || (mode === 'upload' && file ? file.name : '') || 'New analysis'
    try {
      if (mode === 'upload' && file) {
        const result = await createUpload.mutateAsync({
          file,
          title: displayTitle,
        })

        toastAnalysisQueued(displayTitle)
        reset()
        // Go straight to the report page; it will show the AI loader while processing.
        navigate(`/dashboard/analyses/${result.id}`)
      } else {
        await createPaste.mutateAsync({
          title: displayTitle,
          source_type: 'paste',
          raw_text: text.trim(),
        })
        toastAnalysisQueued(displayTitle)
        navigate('/dashboard/analyses')
        reset()
      }
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
              placeholder={mode === 'upload' && file ? file.name : 'e.g. Service Agreement — Acme Corp'}
              className="w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-300"
            />
          </div>

          <AnalysisModeToggle
            mode={mode}
            onChange={(newMode) => {
              setMode(newMode)
              setFile(null)
              setText('')
            }}
          />

          {mode === 'upload' && (
            <UploadDropzone
              file={file}
              onFileSelect={setFile}
            />
          )}

          {mode === 'paste' && (
            <PasteTextInput
              value={text}
              onChange={setText}
            />
          )}

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