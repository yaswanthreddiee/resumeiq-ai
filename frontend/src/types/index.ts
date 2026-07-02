export interface User {
  id: string
  email: string
  name: string
  avatar?: string
  role: 'user' | 'admin'
  createdAt: string
  updatedAt: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface Resume {
  id: string
  userId: string
  fileName: string
  fileUrl: string
  uploadedAt: string
  parsedContent: ResumeParsedContent
  atsScore?: ATSScore
  createdAt: string
  updatedAt: string
}

export interface ResumeParsedContent {
  summary?: string
  skills: string[]
  experience: Experience[]
  education: Education[]
  projects: Project[]
  certifications: Certification[]
}

export interface Experience {
  title: string
  company: string
  startDate: string
  endDate: string
  description: string
}

export interface Education {
  degree: string
  institution: string
  field: string
  graduationDate: string
}

export interface Project {
  name: string
  description: string
  technologies: string[]
  url?: string
}

export interface Certification {
  name: string
  issuer: string
  issueDate: string
  expiryDate?: string
}

export interface ATSScore {
  id: string
  resumeId: string
  overallScore: number
  keywordMatch: number
  grammarScore: number
  formattingScore: number
  actionVerbScore: number
  missingSkills: string[]
  suggestions: string[]
  sectionAnalysis: SectionAnalysis[]
  createdAt: string
}

export interface SectionAnalysis {
  section: string
  score: number
  feedback: string[]
}

export interface JobMatching {
  id: string
  resumeId: string
  jobDescription: string
  matchPercentage: number
  matchedKeywords: string[]
  missingKeywords: string[]
  suggestions: string[]
  createdAt: string
}

export interface Analytics {
  totalResumes: number
  averageAtsScore: number
  totalAnalyses: number
  scoreHistory: ScoreHistory[]
  uploadStats: UploadStats[]
}

export interface ScoreHistory {
  date: string
  score: number
}

export interface UploadStats {
  date: string
  count: number
}

export interface AdminStats {
  totalUsers: number
  totalResumes: number
  totalAnalyses: number
  averageAtsScore: number
  userGrowth: GrowthData[]
}

export interface GrowthData {
  date: string
  users: number
}
