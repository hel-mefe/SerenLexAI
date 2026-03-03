import { useState } from 'react'

export function PasswordInput() {
  const [visible, setVisible] = useState(false)

  return (
    <div className="mb-2">
      <label className="block text-xs font-semibold text-neutral-500 uppercase mb-2">
        Password
      </label>

      <div className="relative">
        <input
          type={visible ? 'text' : 'password'}
          placeholder="••••••••"
          className="w-full px-4 py-3.5 pr-12 rounded-xl bg-neutral-100 border border-border-light focus:ring-2 focus:ring-brand-600/20 outline-none transition"
        />

        <button
          type="button"
          onClick={() => setVisible((v) => !v)}
          className="absolute right-3.5 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-600 transition-colors"
          aria-label="Toggle password visibility"
        >
          {visible ? '🙈' : '👁️'}
        </button>
      </div>

      <div className="flex justify-end mt-3 mb-6">
        <button
          type="button"
          className="text-xs font-medium text-brand-700 hover:text-brand-600 transition-colors"
        >
          Forgot password?
        </button>
      </div>
    </div>
  )
}