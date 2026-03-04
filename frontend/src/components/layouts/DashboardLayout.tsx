import { useEffect, useState } from 'react'
import { Outlet } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Sidebar } from '@/components/dashboard/sidebar/Sidebar'
import { MarketingFooter } from '@/components/marketing/MarketingFooter'

export function DashboardLayout() {
  const [showWelcome, setShowWelcome] = useState(false)

  useEffect(() => {
    const shouldShow = localStorage.getItem('SERENLEXAI_SHOW_WELCOME') === 'true'
    if (!shouldShow) return

    const timer = setTimeout(() => {
      localStorage.removeItem('SERENLEXAI_SHOW_WELCOME')
      setShowWelcome(true)
    }, 1000)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="min-h-screen flex bg-dashboard-gradient relative">
      <Sidebar />

      <div className="flex-1 flex flex-col min-w-0">
        <main className="flex-1 p-8 overflow-auto space-y-8">
          <Outlet />
        </main>
      </div>

      <AnimatePresence>
        {showWelcome && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.4, ease: [0.25, 0.46, 0.45, 0.94] }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-brand-950/95 gap-y-2"
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.96, y: 12 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.98, y: 8 }}
              transition={{ duration: 0.45, ease: [0.25, 0.46, 0.45, 0.94] }}
              className="max-w-2xl w-full mx-4 rounded-3xl border border-white/10 bg-gradient-to-br from-brand-900 via-brand-850 to-brand-700 shadow-glow px-10 py-9 flex flex-col gap-6 text-white"
            >
            <header className="space-y-1.5">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-white/40">
                SerenLexAI · MVP
              </p>
              <h1 className="text-2xl font-bold tracking-tight">
                Welcome to SerenLexAI, Muhammad 👋
              </h1>
              <p className="text-sm text-white/70 max-w-xl mt-4">
                This is a focused MVP, scoped, built, and shipped in 24 hours. Frontend, design, backend, DevOps, infrastructure, and AI integration, all wired together into an architecture built to scale.
              </p>
            </header>

            <section className="space-y-3 text-sm text-white/75">
              <p>
                Is it perfect? Not yet. But that&apos;s the point, it&apos;s designed to move fast and evolve faster. Over the coming days, SerenLexAI will grow well beyond what you&apos;re seeing here: sharper analyses, smoother flows, deeper risk intelligence, and a feature set that&apos;s only getting started.
              </p>
              <p>
                Muhammad, genuinely, thank you for this opportunity. As a McKinsey alum handing this off to a BCG alum, you already know what to expect: no fluff, no filler, just fast, high-quality delivery with the bar set high from day one.
              </p>
              <p>
                That&apos;s the standard this was built to. Hope it shows. 🤝
              </p>
              <p>
                I&apos;m also super excited to work on a product I&apos;ll love and own from day one, which is leveld.ai. I&apos;d love to exceed expectations and build the best quality possible. (Hopefully it&apos;s not 24 hours next time, so we can build something extraordinary. 😄)
              </p>
            </section>

            <div className="pt-2 border-t border-white/10">
              <MarketingFooter />
            </div>

            <div className="flex justify-end pt-2">
              <button
                type="button"
                onClick={() => setShowWelcome(false)}
                className="px-4 py-2 rounded-xl text-sm font-semibold bg-white text-brand-900 hover:bg-slate-100 transition-colors shadow-soft"
              >
                Start exploring
              </button>
            </div>
          </motion.div>
        </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}