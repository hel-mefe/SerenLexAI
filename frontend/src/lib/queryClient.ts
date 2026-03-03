import {
  QueryClient,
  QueryCache,
} from '@tanstack/react-query'

/**
 * Shared React Query client instance for the SerenLex frontend.
 *
 * Centralising the client ensures that caching, retries and error handling
 * strategies are applied consistently across all API consumers.
 */
export const queryClient = new QueryClient({
  queryCache: new QueryCache(),
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      refetchOnWindowFocus: false,
      retry: 2,
    },
  },
})

