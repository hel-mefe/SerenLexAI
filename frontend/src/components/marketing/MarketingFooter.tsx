import { Github, Linkedin, Globe } from 'lucide-react'

export function MarketingFooter() {
  return (
    <div className="">
      <div className="pt-6 text-xs text-white/30 leading-relaxed">
        <div className="mt-3 flex flex-wrap items-center justify-between gap-4 text-white/40">
          <div className="flex items-center gap-4">
          <span className="text-[11px] tracking-wider text-white/25">
            Social links:
          </span>

          <div className="flex justify-center items-center gap-3">
            <a
              href="https://hel-mefe.me"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white transition-colors flex justify-center items-center gap-2"
              aria-label="Portfolio"
            >
              <Globe className="w-4 h-4" />
              <p>Portfolio</p>
            </a>

            <a
              href="https://linkedin.com/in/hicham-elmefeddel"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white transition-colors flex justify-center items-center gap-2"
              aria-label="LinkedIn"
            >
              <Linkedin className="w-4 h-4" />
              <p>Linkedin</p>
            </a>

            <a
              href="https://github.com/hel-mefe"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white transition-colors flex justify-center items-center gap-2"
              aria-label="GitHub"
            >
              <Github className="w-4 h-4" />
              <p>Github</p>
            </a>
          </div>
          </div>
          <span className="text-[11px] text-white/40">All rights reserved to SerenLexAI</span>
        </div>

      </div>

    </div>
  )
}