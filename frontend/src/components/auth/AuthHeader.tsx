// src/components/auth/AuthHeader.tsx

import { useState } from 'react'
import { RequestAccessModal } from '@/components/modals/RequestAccessModal'

export function AuthHeader() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <div className="flex items-center justify-end px-10 pt-8">
        <span className="text-sm text-neutral-400 mr-2">
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

      <RequestAccessModal
        open={open}
        onClose={() => setOpen(false)}
      />
    </>
  )
}