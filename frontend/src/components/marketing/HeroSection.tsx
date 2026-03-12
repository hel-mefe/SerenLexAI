import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

const TYPED_PHRASE = 'Miss nothing.'
const TYPING_SPEED = 60

export function HeroSection() {
  const [typedText, setTypedText] = useState('')

  useEffect(() => {
    let frame: number
    let index = 0

    const step = () => {
      if (index <= TYPED_PHRASE.length) {
        setTypedText(TYPED_PHRASE.slice(0, index))
        index += 1
        frame = window.setTimeout(step, TYPING_SPEED)
      }
    }

    step()

    return () => {
      window.clearTimeout(frame)
    }
  }, [])

  return (
    <section className="relative flex-1 w-full min-w-full flex flex-col items-center justify-center px-4 hero-grid-bg">
      <div className="mx-auto max-w-4xl text-center fade-in-up">
        <h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl md:text-6xl">
          Read every clause.
          <span className="mt-2 block text-white/50">
            <span>{typedText}</span>
            <span className="inline-block w-3 animate-pulse align-baseline">|</span>
          </span>
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-lg text-white/60 fade-in-up-delay">
          SerenLexAI is the AI-powered contract review tool that flags risks,
          explains clauses in plain English, and helps non-lawyers sign with confidence.
        </p>
        <div className="mt-10 flex flex-wrap items-center justify-center gap-4 fade-in-up-delay">
          <Link
            to="/signin"
            className="rounded-xl bg-sidebar-gradient px-6 py-3 text-base font-semibold text-white shadow-lg hover:opacity-90 transition-opacity"
          >
            Get started
          </Link>
          <a
            href="#features"
            className="rounded-xl border border-white/20 bg-white/5 px-6 py-3 text-base font-semibold text-white hover:bg-white/10 transition-colors"
          >
            See how it works
          </a>
        </div>
      </div>
    </section>
  )
}
