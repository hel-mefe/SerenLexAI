import { useState } from 'react'

type Props = {
  field: any
}

export function PasswordInput({ field }: Props) {
  const [visible, setVisible] = useState(false)

  return (
    <div className="mb-2">
      <label className="block text-xs font-semibold text-neutral-500 uppercase mb-2">
        Password
      </label>

      <div className="relative">
        <input
          type={visible ? 'text' : 'password'}
          value={field.state.value}
          onChange={(e) => field.handleChange(e.target.value)}
          onBlur={field.handleBlur}
          placeholder="••••••••"
          className="w-full px-4 py-3.5 rounded-xl text-sm text-slate-800 placeholder-slate-300 outline-none transition-all pr-12"
          style={{
            background: 'rgb(247, 248, 250)',
            border: '1.5px solid rgb(234, 236, 240)',
          }}
        />

        <button
          type="button"
          onClick={() => setVisible((v) => !v)}
          className="absolute right-3.5 top-1/2 -translate-y-1/2 w-6 h-6 flex items-center justify-center text-slate-400 hover:text-slate-600 cursor-pointer transition-colors"
          aria-label="Toggle password visibility"
        >
          {visible ? '🙈' : '👁️'}
        </button>
      </div>

      {field.state.meta.errors?.length ? (
        <p className="text-xs text-risk-high mt-2">
          {field.state.meta.errors[0]}
        </p>
      ) : null}

      <div className="flex justify-end mt-3 mb-6">
        <button
          type="button"
          className="text-xs font-medium cursor-pointer transition-colors"
          style={{ color: 'rgb(26, 31, 46)' }}
        >
          Forgot password?
        </button>
      </div>
    </div>
  )
}