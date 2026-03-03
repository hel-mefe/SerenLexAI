import { useState } from 'react'
import { motion } from 'framer-motion'

import { NewAnalysisHeader } from '@/components/newanalysis/NewAnalysisHeader'
import { AnalysisModeToggle } from '@/components/newanalysis/AnalaysisModeToggle'
import { UploadDropzone } from '@/components/newanalysis/UploadDropZone'
import { StartAnalysisButton } from '@/components/newanalysis/StartAnalysisbutton'
import { FeatureHighlights } from '@/components/newanalysis/FeatureHighlights'

export default function NewAnalysisPage() {
  const [mode, setMode] = useState<'upload' | 'paste'>('upload')
  const [file, setFile] = useState<File | null>(null)

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
          <AnalysisModeToggle
            mode={mode}
            onChange={setMode}
          />

          {mode === 'upload' && (
            <UploadDropzone
              file={file}
              onFileSelect={setFile}
            />
          )}

          <StartAnalysisButton disabled={!file} />

          <FeatureHighlights />
        </div>
      </main>
    </motion.div>
  )
}