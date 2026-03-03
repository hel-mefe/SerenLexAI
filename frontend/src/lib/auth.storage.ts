import { AUTH_KEY } from "@/config"

export const authStorage = {
  login() {
    localStorage.setItem(AUTH_KEY, 'true')
  },

  logout() {
    localStorage.removeItem(AUTH_KEY)
  },

  isAuthenticated() {
    return localStorage.getItem(AUTH_KEY) === 'true'
  },
}