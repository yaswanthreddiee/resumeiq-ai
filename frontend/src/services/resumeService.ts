import api from './authService'
import { Resume, ATSScore, JobMatching } from '../types'

export const uploadResume = async (file: File): Promise<Resume> => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await api.post<Resume>('/resumes/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const getResumes = async (): Promise<Resume[]> => {
  const response = await api.get<Resume[]>('/resumes')
  return response.data
}

export const getResume = async (id: string): Promise<Resume> => {
  const response = await api.get<Resume>(`/resumes/${id}`)
  return response.data
}

export const deleteResume = async (id: string): Promise<{ message: string }> => {
  const response = await api.delete(`/resumes/${id}`)
  return response.data
}

export const analyzeATS = async (resumeId: string): Promise<ATSScore> => {
  const response = await api.post<ATSScore>(`/resumes/${resumeId}/analyze-ats`)
  return response.data
}

export const matchJobDescription = async (
  resumeId: string,
  jobDescription: string
): Promise<JobMatching> => {
  const response = await api.post<JobMatching>(`/resumes/${resumeId}/match-job`, {
    job_description: jobDescription,
  })
  return response.data
}

export const getATSScore = async (resumeId: string): Promise<ATSScore> => {
  const response = await api.get<ATSScore>(`/resumes/${resumeId}/ats-score`)
  return response.data
}

export const getJobMatching = async (resumeId: string): Promise<JobMatching> => {
  const response = await api.get<JobMatching>(`/resumes/${resumeId}/job-matching`)
  return response.data
}

export default api
