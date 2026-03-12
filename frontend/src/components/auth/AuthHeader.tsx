// src/components/auth/AuthHeader.tsx

import { useState } from 'react'
import { Link } from 'react-router-dom'
import { RequestAccessModal } from '@/components/modals/RequestAccessModal'

export function AuthHeader() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <div className="flex items-center justify-between px-10 pt-8">
        <Link to="/" className="text-sm text-neutral-500 hover:text-neutral-700 transition-colors">
          Back to home
        </Link>
        <div className="flex items-center gap-2">
        <span className="text-sm text-neutral-400">
          New here?
        </span>
        <button
          type="button"
          onClick={() => setOpen(true)}
          className="text-sm cursor-pointer font-semibold text-neutral-900 hover:text-neutral-700 transition-colors"
        >
          Request Access
        </button>
        </div>
      </div>

      <RequestAccessModal
        open={open}
        onClose={() => setOpen(false)}
      />
    </>
  )
}