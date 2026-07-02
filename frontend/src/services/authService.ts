import axios from 'axios'
import { User, AuthResponse } from '../types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_URL,
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const signup = async (data: {
  email: string
  password: string
  name: string
}): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>('/auth/signup', data)
  return response.data
}

export const login = async (data: {
  email: string
  password: string
}): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>('/auth/login', data)
  return response.data
}

export const getCurrentUser = async (): Promise<User> => {
  const response = await api.get<User>('/auth/me')
  return response.data
}

export const forgotPassword = async (email: string): Promise<{ message: string }> => {
  const response = await api.post('/auth/forgot-password', { email })
  return response.data
}

export const resetPassword = async (token: string, newPassword: string): Promise<{ message: string }> => {
  const response = await api.post('/auth/reset-password', { token, new_password: newPassword })
  return response.data
}

export const updateProfile = async (data: Partial<User>): Promise<User> => {
  const response = await api.put<User>('/auth/profile', data)
  return response.data
}

export default api
