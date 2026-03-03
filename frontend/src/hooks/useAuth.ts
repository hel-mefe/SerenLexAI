import { useNavigate } from 'react-router-dom'
import { authStorage } from '@/lib/auth.storage'

export function useAuth() {
  const navigate = useNavigate()

  const login = () => {
    authStorage.login()
    navigate('/dashboard/overview')
  }

  const logout = () => {
    authStorage.logout()
    navigate('/login')
  }

  const isAuthenticated = authStorage.isAuthenticated()

  return {
    login,
    logout,
    isAuthenticated,
  }
}