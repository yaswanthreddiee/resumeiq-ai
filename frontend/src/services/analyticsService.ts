import api from './api'
import { Analytics, AdminStats } from '../types'

export async function getUserAnalytics(): Promise<Analytics> {
  const response = await api.get('/analytics')
  return response.data
}

export async function getAdminAnalytics(): Promise<AdminStats> {
  const response = await api.get('/analytics/admin/analytics')
  return response.data
}
