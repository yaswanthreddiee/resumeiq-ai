import React, { createContext, useContext, useState, useEffect } from 'react'
import { User, AuthResponse } from '../types'
import * as authService from '../services/authService'

interface AuthContextType {
  user: User | null
  loading: boolean
  error: string | null
  isAuthenticated: boolean
  signup: (email: string, password: string, name: string) => Promise<void>
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  clearError: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Check if user is already authenticated on mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('access_token')
        if (token) {
          const currentUser = await authService.getCurrentUser()
          setUser(currentUser)
        }
      } catch (err) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
      } finally {
        setLoading(false)
      }
    }

    checkAuth()
  }, [])

  const signup = async (email: string, password: string, name: string) => {
    try {
      setError(null)
      const response: AuthResponse = await authService.signup({ email, password, name })
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))
      setUser(response.user)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Signup failed'
      setError(message)
      throw err
    }
  }

  const login = async (email: string, password: string) => {
    try {
      setError(null)
      const response: AuthResponse = await authService.login({ email, password })
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))
      setUser(response.user)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Login failed'
      setError(message)
      throw err
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    setUser(null)
  }

  const clearError = () => setError(null)

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        error,
        isAuthenticated: !!user,
        signup,
        login,
        logout,
        clearError,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
