import { MarketingFooter } from "./MarketingFooter";
import { StatsGroup } from "./StatsGroup";

export function HeroContent() {
  return (
    <div className="flex flex-col gap-y-12 justify-center flex-1 px-14 pb-6">
        <div className="flex flex-col">
            <h1 className="text-4xl xl:text-[42px] font-bold leading-tight mb-4">
                Read Every Clause.
                <span className="block text-white/40">
                Miss Nothing.
                </span>
            </h1>
            <p className="text-sm text-white/50 max-w-[380px] mb-6">
                Project managers and commercial leads sign contracts
                without legal counsel every day.
            </p>
            <p className="text-sm text-white/60 max-w-[420px] leading-relaxed">
                SerenLexAI is the ultimate AI-powered tool for contract review: it flags risks, explains clauses in plain English, and helps non-lawyers sign with confidence.
            </p>
        </div>

    <div className="footer flex flex-col gap-y-2">
      <StatsGroup />

      <MarketingFooter />

    </div>

    </div>
  )
}