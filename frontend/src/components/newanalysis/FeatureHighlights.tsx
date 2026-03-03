import {
  ShieldCheck,
  Brain,
  Clock,
} from 'lucide-react'

export function FeatureHighlights() {
  const features = [
    {
      icon: ShieldCheck,
      title: 'Secure Processing',
      desc: 'End-to-end encrypted, never stored',
    },
    {
      icon: Brain,
      title: 'AI-Powered',
      desc: 'Advanced clause detection & scoring',
    },
    {
      icon: Clock,
      title: 'Fast Results',
      desc: 'Comprehensive analysis in under 2 min',
    },
  ]

  return (
    <div className="grid grid-cols-3 gap-4 mt-10">
      {features.map((feature) => {
        const Icon = feature.icon
        return (
          <div
            key={feature.title}
            className="rounded-2xl p-5 text-center bg-white/75 border border-black/5 backdrop-blur"
          >
            <div className="w-10 h-10 flex items-center justify-center rounded-xl bg-slate-100 mx-auto mb-3">
              <Icon className="w-5 h-5 text-slate-700" />
            </div>

            <h4 className="text-sm font-bold text-slate-900 mb-1">
              {feature.title}
            </h4>

            <p className="text-xs text-slate-500">
              {feature.desc}
            </p>
          </div>
        )
      })}
    </div>
  )
}