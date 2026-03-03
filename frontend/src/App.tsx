import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-auth-gradient">
      <div className="bg-brand-700 rounded-3xl shadow-xl p-10">
        <h1 className="text-4xl text-risk-high font-bold text-brand-900">
          SerenLexAI
        </h1>
        <p className="text-risk-medium mt-4">
          Tailwind v4 theme works
        </p>
      </div>
    </div>
  )
}

export default App