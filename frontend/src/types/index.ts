export interface User {
  _id?: string
  id?: string
  email: string
  name: string
  role: 'user' | 'admin'
  created_at?: string
  updated_at?: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: User
}

export interface ResumeParsedContent {
  summary?: string
  skills: string[]
  experience: any[]
  education: any[]
  projects: any[]
  certifications: any[]
}

export interface ATSScore {
  id?: string
  resume_id?: string
  overall_score: number
  keyword_match: number
  grammar_score: number
  formatting_score: number
  action_verb_score: number
  missing_skills: string[]
  suggestions: string[]
  section_analysis: any[]
  created_at?: string
}

export interface JobMatching {
  id?: string
  resume_id?: string
  job_description: string
  match_percentage: number
  matched_keywords: string[]
  missing_keywords: string[]
  suggestions: string[]
  created_at?: string
}

export interface Resume {
  id: string
  _id?: string
  user_id?: string
  file_name: string
  file_url: string
  uploaded_at: string
  parsed_content?: ResumeParsedContent
  ats_score?: ATSScore
  created_at?: string
  updated_at?: string
}

export interface Analytics {
  total_resumes: number
  average_ats_score: number
  total_analyses: number
  score_history: Array<{ date: string; score: number }>
  upload_stats: Array<{ date: string; count: number }>
}

export interface AdminStats {
  total_users: number
  total_resumes: number
  total_analyses: number
  average_ats_score: number
  user_growth: Array<{ date: string; users: number }>
}
