import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { User, TokenResponse } from '../types'
import * as authService from '../services/authService'

interface AuthContextType {
  user: User | null
  token: string | null
  loading: boolean
  signup: (email: string, password: string, name: string) => Promise<void>
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Initialize from localStorage
    const savedToken = localStorage.getItem('access_token')
    const savedUser = localStorage.getItem('user')
    
    if (savedToken && savedUser) {
      setToken(savedToken)
      setUser(JSON.parse(savedUser))
    }
    setLoading(false)
  }, [])

  const signup = async (email: string, password: string, name: string) => {
    const response = await authService.signup(email, password, name)
    setToken(response.access_token)
    setUser(response.user)
  }

  const login = async (email: string, password: string) => {
    const response = await authService.login(email, password)
    setToken(response.access_token)
    setUser(response.user)
  }

  const logout = () => {
    authService.logout()
    setToken(null)
    setUser(null)
  }

  const value: AuthContextType = {
    user,
    token,
    loading,
    signup,
    login,
    logout,
    isAuthenticated: !!token,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
