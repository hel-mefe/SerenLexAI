import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },

      colors: {
        brand: {
          950: '#0D1117',
          900: '#0F1320',
          850: '#121826',
          800: '#161B27',
          700: '#1A1F2E',
          600: '#2D3550',
        },

        surface: {
          DEFAULT: '#F4F6F8',
          subtle: '#EEF1F4',
          card: '#FFFFFF',
        },

        risk: {
          high: '#EF4444',
          medium: '#F59E0B',
          low: '#10B981',
        },
      },

      backgroundImage: {
        'auth-gradient':
          'linear-gradient(135deg, #0D1117 0%, #161B27 40%, #1A2035 70%, #0F1320 100%)',

        'card-gradient':
          'linear-gradient(135deg, #1A1F2E 0%, #2D3550 100%)',

        'subtle-gradient':
          'linear-gradient(160deg, #1A1F2E 0%, #141824 55%, #0F1320 100%)',
      },

      boxShadow: {
        soft: '0 10px 30px rgba(0,0,0,0.08)',
        glow: '0 40px 100px rgba(0,0,0,0.6)',
      },

      borderRadius: {
        '3xl': '1.75rem',
      },
    },
  },
} satisfies Config