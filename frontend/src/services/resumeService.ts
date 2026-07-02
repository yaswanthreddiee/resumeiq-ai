import api from './api'
import { Resume, ATSScore, JobMatching } from '../types'

export async function uploadResume(file: File): Promise<Resume> {
  const formData = new FormData()
  formData.append('file', file)
  const response = await api.post('/resumes/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

export async function getResumes(): Promise<Resume[]> {
  const response = await api.get('/resumes')
  return response.data
}

export async function getResume(resumeId: string): Promise<Resume> {
  const response = await api.get(`/resumes/${resumeId}`)
  return response.data
}

export async function deleteResume(resumeId: string): Promise<{ message: string }> {
  const response = await api.delete(`/resumes/${resumeId}`)
  return response.data
}

export async function analyzeATS(resumeId: string): Promise<ATSScore> {
  const response = await api.post(`/resumes/${resumeId}/analyze-ats`)
  return response.data
}

export async function matchJobDescription(resumeId: string, jobDescription: string): Promise<JobMatching> {
  const response = await api.post(`/resumes/${resumeId}/match-job`, { job_description: jobDescription })
  return response.data
}

export async function getATSScore(resumeId: string): Promise<ATSScore> {
  const response = await api.get(`/resumes/${resumeId}/ats-score`)
  return response.data
}

export async function getJobMatching(resumeId: string): Promise<JobMatching> {
  const response = await api.get(`/resumes/${resumeId}/job-matching`)
  return response.data
}
