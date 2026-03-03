import axios, { type AxiosInstance } from 'axios'

/**
 * Base URL for the SerenLex backend.
 *
 * Prefer configuring `VITE_API_BASE_URL` in the frontend `.env`, for example:
 *
 * - `VITE_API_BASE_URL=http://localhost:8000/api/v1`
 *
 * When the variable is not set we default to `/api/v1` so that a dev proxy or
 * same-origin deployment can be used without additional configuration.
 *
 * @constant
 */
const API_BASE_URL = 'http://localhost:8000/api/v1'
  // import.meta.env['VITE_API_BASE_URL']?.replace(/\/+$/, '') ?? '/api/v1'

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
  timeout: 15_000,
})

