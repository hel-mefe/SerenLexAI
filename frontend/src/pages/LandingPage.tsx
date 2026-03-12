import { MarketingNavbar } from '@/components/marketing/MarketingNavbar'
import { HeroSection } from '@/components/marketing/HeroSection'
import { MarketingFooter } from '@/components/marketing/MarketingFooter'

export function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-brand-950">
      <MarketingNavbar />
      <main className="flex-1 flex flex-col">
        <HeroSection />
      </main>
      <footer className="flex-shrink-0 bg-brand-950 py-8">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <MarketingFooter />
        </div>
      </footer>
    </div>
  )
}
