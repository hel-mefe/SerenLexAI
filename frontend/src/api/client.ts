import axios, { type AxiosInstance } from 'axios'

/**
 * Base URL for the SerenLex backend.
 * Set VITE_API_BASE_URL in frontend/.env (see .env.example).
 * When unset, defaults to http://localhost:8000/api/v1 for local dev.
 */
const API_BASE_URL =
  (import.meta.env['VITE_API_BASE_URL']?.replace(/\/+$/, '') as string | undefined) ??
  'http://localhost:8000/api/v1'

/**
 * Shared Axios client instance for the SerenLex backend.
 *
 * All API modules should use this client so that concerns such as auth
 * headers, tracing and error handling can be configured centrally here.
 *
 * @constant
 */
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  // Some endpoints (PDF upload + background enqueue) can take longer;
  // allow up to 60s before timing out on the client.
  timeout: 60_000,
})

