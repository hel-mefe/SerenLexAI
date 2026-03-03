import { ArrowLeft, Download, Plus } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { AnalysisTitleBlock } from './AnalysisTitleBlock'

type Props = {
  analysisId?: string | undefined
}

export function AnalysisTopBar({ analysisId }: Props) {
  const navigate = useNavigate()

  console.log(analysisId)
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
          title={`Service Agreement — Acme Corp`}
          riskLevel="High"
          date="Dec 18, 2024 at 14:32"
          reviewedCount={12}
        />
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-3">
        <button className="flex cursor-pointer text-white items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold text-slate-600 hover:bg-gray-600 transition border border-slate-200">
          <Download className="w-4 h-4" />
          Export PDF
        </button>

        <button
          onClick={() => navigate('/dashboard/upload')}
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