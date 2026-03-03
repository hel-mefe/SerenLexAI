import { BrandLogo } from "./BrandLogo"
import { HeroContent } from "./HeroContent"

export function MarketingPanel() {
  return (
    <div className="hidden lg:flex lg:w-[52%] border-red-400 rounded-l-4xl flex-col bg-auth-gradient text-white relative">
      <BrandLogo />
      <HeroContent />
    </div>
  )
}