import api from './authService'
import { Analytics, AdminStats } from '../types'

export const getUserAnalytics = async (): Promise<Analytics> => {
  const response = await api.get<Analytics>('/analytics')
  return response.data
}

export const getAdminAnalytics = async (): Promise<AdminStats> => {
  const response = await api.get<AdminStats>('/admin/analytics')
  return response.data
}

export const getUsersCount = async (): Promise<{ count: number }> => {
  const response = await api.get('/admin/users/count')
  return response.data
}

export const getResumesCount = async (): Promise<{ count: number }> => {
  const response = await api.get('/admin/resumes/count')
  return response.data
}

export const getAnalysesCount = async (): Promise<{ count: number }> => {
  const response = await api.get('/admin/analyses/count')
  return response.data
}
