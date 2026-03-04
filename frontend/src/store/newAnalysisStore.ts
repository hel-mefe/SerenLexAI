import { create } from 'zustand'

export type NewAnalysisMode = 'upload' | 'paste'

interface NewAnalysisState {
  mode: NewAnalysisMode
  title: string
  file: File | null
  text: string
  setMode: (mode: NewAnalysisMode) => void
  setTitle: (title: string) => void
  setFile: (file: File | null) => void
  setText: (text: string) => void
  reset: () => void
}

const initialState: Pick<
  NewAnalysisState,
  'mode' | 'title' | 'file' | 'text'
> = {
  mode: 'upload',
  title: '',
  file: null,
  text: '',
}

export const useNewAnalysisStore = create<NewAnalysisState>(
  (set) => ({
    ...initialState,
    setMode: (mode) => set({ mode }),
    setTitle: (title) => set({ title }),
    setFile: (file) => set({ file }),
    setText: (text) => set({ text }),
    reset: () => set(initialState),
  }),
)

