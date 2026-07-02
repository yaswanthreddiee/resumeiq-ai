import api from './api'
import { User, TokenResponse } from '../types'

export async function signup(email: string, password: string, name: string): Promise<TokenResponse> {
  const response = await api.post('/auth/signup', { email, password, name })
  const data = response.data
  localStorage.setItem('access_token', data.access_token)
  localStorage.setItem('user', JSON.stringify(data.user))
  return data
}

export async function login(email: string, password: string): Promise<TokenResponse> {
  const response = await api.post('/auth/login', { email, password })
  const data = response.data
  localStorage.setItem('access_token', data.access_token)
  localStorage.setItem('user', JSON.stringify(data.user))
  return data
}

export async function getCurrentUser(): Promise<User> {
  const response = await api.get('/auth/me')
  return response.data
}

export async function updateProfile(data: { name?: string; email?: string }): Promise<User> {
  const response = await api.put('/auth/profile', data)
  const user = response.data
  localStorage.setItem('user', JSON.stringify(user))
  return user
}

export async function logout(): Promise<void> {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user')
}

export async function forgotPassword(email: string): Promise<{ message: string }> {
  const response = await api.post('/auth/forgot-password', { email })
  return response.data
}

export async function resetPassword(token: string, newPassword: string): Promise<{ message: string }> {
  const response = await api.post('/auth/reset-password', { token, new_password: newPassword })
  return response.data
}
