import { useState } from 'react'
import { ArrowLeft, Download, Plus } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { AnalysisTitleBlock } from './AnalysisTitleBlock'

import type { SeverityLevel } from '@/types/analysis'
import { downloadAnalysisReportPdf } from '@/api/analysis/api'

type Props = {
  analysisId: string
  title: string
  date: string
  reviewedCount: number
  overallRisk: SeverityLevel | null
  status: string
  sourceType: string
  originalFilename: string | null
}

export function AnalysisTopBar({
  analysisId,
  title,
  date,
  reviewedCount,
  overallRisk,
  status,
  sourceType,
  originalFilename,
}: Props) {
  const navigate = useNavigate()
  const [downloading, setDownloading] = useState(false)

  const canExportPdf = status === 'completed'

  const handleExportPdf = async () => {
    if (!canExportPdf || downloading) return
    setDownloading(true)
    try {
      const baseName = (originalFilename || title || analysisId).trim()
      await downloadAnalysisReportPdf(analysisId, baseName || undefined)
    } finally {
      setDownloading(false)
    }
  }

  return (
    <motion.header
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="
        sticky top-0 z-20
        flex items-center justify-between
        px-12 py-8 rounded-4xl
        bg-gray-900 backdrop-blur-xl
        border-b border-black/5
      "
    >
      {/* Left Section */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => navigate(-1)}
          className="w-9 h-9 flex items-center justify-center rounded-xl cursor-pointer text-white hover:bg-gray-700 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>

        <AnalysisTitleBlock
          title={title}
          riskLevel={overallRisk}
          status={status}
          date={date}
          reviewedCount={reviewedCount}
        />
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-3">
        {canExportPdf && (
          <button
            type="button"
            onClick={handleExportPdf}
            disabled={downloading}
            className="flex cursor-pointer text-white items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold hover:bg-gray-600 transition border border-slate-200 disabled:opacity-60"
          >
            <Download className="w-4 h-4" />
            {downloading ? 'Downloading…' : 'Export PDF'}
          </button>
        )}

        <button
          onClick={() => navigate('/dashboard/analyses/new')}
          className="
            flex items-center gap-2 px-4 py-2 rounded-xl cursor-pointer
            text-sm font-semibold text-white
            bg-gradient-to-br from-[#1a1f2e] to-[#2d3550] text-white
            hover:shadow-lg transition
          "
        >
          <Plus className="w-4 h-4" />
          New Analysis
        </button>
      </div>
    </motion.header>
  )
}