import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

export function MarketingNavbar() {
  const [atTop, setAtTop] = useState(true)

  useEffect(() => {
    const onScroll = () => setAtTop(window.scrollY < 8)
    window.addEventListener('scroll', onScroll, { passive: true })
    onScroll()
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-[background,border-color] duration-300 ${
        atTop
          ? 'border-b border-transparent bg-transparent'
          : 'border-b border-white/10 bg-sidebar-gradient backdrop-blur-md'
      }`}
    >
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-x-2">
          <span className="font-semibold text-xl tracking-tight text-white">SerenLexAI</span>
        </Link>
        <nav>
          <Link to="/signin" className="rounded-lg bg-sidebar-gradient px-4 py-2 text-sm font-medium text-white hover:opacity-90 transition-opacity">
            Get started
          </Link>
        </nav>
      </div>
    </header>
  )
}
