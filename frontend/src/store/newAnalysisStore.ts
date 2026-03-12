import { create } from 'zustand'

interface NewAnalysisState {
  title: string
  file: File | null
  setTitle: (title: string) => void
  setFile: (file: File | null) => void
  reset: () => void
}

const initialState: Pick<NewAnalysisState, 'title' | 'file'> = {
  title: '',
  file: null,
}

export const useNewAnalysisStore = create<NewAnalysisState>((set) => ({
  ...initialState,
  setTitle: (title) => set({ title }),
  setFile: (file) => set({ file }),
  reset: () => set(initialState),
}))
