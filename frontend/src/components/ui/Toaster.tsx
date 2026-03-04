import { Toaster as HotToaster } from 'react-hot-toast'

/**
 * Global toast container with SerenLex brand styling.
 * Renders at top-center with elegant, modern defaults.
 */
const toastOptions = {
  duration: 5000,
  position: 'top-center' as const,
  style: {
    background:
      'linear-gradient(135deg, var(--color-brand-700), var(--color-brand-600))',
    color: '#ffffff',
    borderRadius: '1rem',
    border: '1px solid rgba(255, 255, 255, 0.08)',
    boxShadow: '0 10px 40px -10px rgba(15, 23, 42, 0.35)',
    padding: '0.875rem 1.25rem',
    fontSize: '0.875rem',
    fontWeight: 500,
    maxWidth: '420px',
  },
  success: {
    iconTheme: {
      primary: 'var(--color-risk-low)',
      secondary: 'var(--color-surface-card)',
    },
  },
  error: {
    iconTheme: {
      primary: 'var(--color-risk-high)',
      secondary: 'var(--color-surface-card)',
    },
  },
  loading: {
    iconTheme: {
      primary: 'var(--color-brand-700)',
      secondary: 'var(--color-neutral-200)',
    },
  },
}

export function Toaster() {
  return (
    <HotToaster
      position={toastOptions.position}
      toastOptions={{
        duration: toastOptions.duration,
        style: toastOptions.style,
        success: toastOptions.success,
        error: toastOptions.error,
        loading: toastOptions.loading,
      }}
      containerStyle={{
        top: 24,
      }}
    />
  )
}
