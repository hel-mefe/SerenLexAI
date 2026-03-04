import { AUTH_KEY } from "@/config"

export const authStorage = {
  login() {
    localStorage.setItem(AUTH_KEY, 'true')
    localStorage.setItem('SERENLEXAI_SHOW_WELCOME', 'true')
  },

  logout() {
    localStorage.removeItem(AUTH_KEY)
  },

  isAuthenticated() {
    return localStorage.getItem(AUTH_KEY) === 'true'
  },
}