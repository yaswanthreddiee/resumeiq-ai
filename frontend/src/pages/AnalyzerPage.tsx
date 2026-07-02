import { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardHeader, CardTitle, CardDescription, CardFooter } from '../components/Card'
import { Button } from '../components/Button'
import { Input } from '../components/Input'
import FileUpload from '../components/FileUpload'
import LoadingSpinner from '../components/LoadingSpinner'
import { pageVariants, containerVariants, itemVariants } from '../animations/pageTransitions'
import * as resumeService from '../services/resumeService'
import { ATSScore, JobMatching } from '../types'
import { CheckCircle, AlertCircle, Sparkles, Zap } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts'

const AnalyzerPage: React.FC = () => {
  const [step, setStep] = useState<'upload' | 'analysis' | 'results'>('upload')
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [atsScore, setAtsScore] = useState<ATSScore | null>(null)
  const [jobDescription, setJobDescription] = useState('')
  const [jobMatching, setJobMatching] = useState<JobMatching | null>(null)
  const [resumeId, setResumeId] = useState<string | null>(null)

  const handleFileSelect = (file: File) => {
    setSelectedFile(file)
    setError(null)
  }

  const handleUploadAndAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select a file')
      return
    }

    setLoading(true)
    try {
      // Upload resume
      const resume = await resumeService.uploadResume(selectedFile)
      setResumeId(resume.id)

      // Analyze ATS
      const atsAnalysis = await resumeService.analyzeATS(resume.id)
      setAtsScore(atsAnalysis)

      setStep('results')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed')
    } finally {
      setLoading(false)
    }
  }

  const handleJobMatching = async () => {
    if (!jobDescription.trim() || !resumeId) {
      setError('Please enter a job description')
      return
    }

    setLoading(true)
    try {
      const matching = await resumeService.matchJobDescription(resumeId, jobDescription)
      setJobMatching(matching)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Job matching failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <motion.div
      initial="initial"
      animate="animate"
      exit="exit"
      variants={pageVariants}
      className="min-h-screen bg-background py-8 px-4"
    >
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          className="mb-8"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div variants={itemVariants}>
            <h1 className="text-4xl font-bold mb-2">Resume Analyzer</h1>
            <p className="text-muted-foreground">Upload your resume and get instant ATS analysis</p>
          </motion.div>
        </motion.div>

        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6 p-4 bg-destructive/10 border border-destructive/50 rounded-lg flex items-start space-x-3"
          >
            <AlertCircle size={20} className="text-destructive mt-0.5 flex-shrink-0" />
            <p className="text-destructive text-sm">{error}</p>
          </motion.div>
        )}

        {step === 'upload' && (
          <motion.div variants={containerVariants} initial="hidden" animate="visible" className="space-y-6">
            <motion.div variants={itemVariants}>
              <Card className="p-8">
                <CardHeader className="px-0 pt-0 mb-6">
                  <CardTitle>Upload Your Resume</CardTitle>
                  <CardDescription>PDF or DOCX format, up to 10MB</CardDescription>
                </CardHeader>
                <FileUpload onFileSelect={handleFileSelect} />
              </Card>
            </motion.div>

            <motion.div variants={itemVariants} className="flex justify-center">
              <Button
                size="lg"
                onClick={handleUploadAndAnalyze}
                disabled={!selectedFile || loading}
                className="rounded-lg flex items-center space-x-2"
              >
                {loading ? (
                  <>
                    <LoadingSpinner size="sm" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <Zap size={20} />
                    <span>Analyze Resume</span>
                  </>
                )}
              </Button>
            </motion.div>
          </motion.div>
        )}

        {step === 'results' && atsScore && (
          <motion.div variants={containerVariants} initial="hidden" animate="visible" className="space-y-6">
            {/* ATS Score Card */}
            <motion.div variants={itemVariants}>
              <Card className="p-8 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-accent/10 to-secondary/10 pointer-events-none" />
                <div className="relative z-10">
                  <div className="text-center">
                    <p className="text-muted-foreground mb-2">Overall ATS Score</p>
                    <div className="text-6xl font-bold text-accent mb-4">{atsScore.overallScore}%</div>
                    <p className="text-foreground mb-6">
                      {atsScore.overallScore >= 70
                        ? '✨ Great! Your resume is ATS-friendly'
                        : '⚠️ There is room for improvement'}
                    </p>
                  </div>
                </div>
              </Card>
            </motion.div>

            {/* Detailed Scores */}
            <motion.div variants={itemVariants}>
              <Card className="p-6">
                <CardHeader className="px-0 pt-0 mb-6">
                  <CardTitle>Detailed Analysis</CardTitle>
                </CardHeader>
                <div className="grid md:grid-cols-2 gap-6">
                  {[
                    { label: 'Keyword Match', value: atsScore.keywordMatch },
                    { label: 'Grammar Score', value: atsScore.grammarScore },
                    { label: 'Formatting Score', value: atsScore.formattingScore },
                    { label: 'Action Verb Score', value: atsScore.actionVerbScore },
                  ].map((item) => (
                    <div key={item.label} className="p-4 border border-card rounded-lg">
                      <p className="text-muted-foreground text-sm font-medium mb-2">{item.label}</p>
                      <div className="w-full bg-muted rounded-full h-2">
                        <div
                          className="h-2 bg-accent rounded-full transition-all duration-500"
                          style={{ width: `${item.value}%` }}
                        />
                      </div>
                      <p className="text-lg font-bold mt-2">{item.value}%</p>
                    </div>
                  ))}
                </div>
              </Card>
            </motion.div>

            {/* Missing Skills */}
            {atsScore.missingSkills && atsScore.missingSkills.length > 0 && (
              <motion.div variants={itemVariants}>
                <Card className="p-6">
                  <CardHeader className="px-0 pt-0 mb-4">
                    <CardTitle>Missing Skills</CardTitle>
                  </CardHeader>
                  <div className="flex flex-wrap gap-2">
                    {atsScore.missingSkills.map((skill) => (
                      <span key={skill} className="px-3 py-1 bg-accent/10 text-accent rounded-full text-sm border border-accent/20">
                        {skill}
                      </span>
                    ))}
                  </div>
                </Card>
              </motion.div>
            )}

            {/* Suggestions */}
            {atsScore.suggestions && atsScore.suggestions.length > 0 && (
              <motion.div variants={itemVariants}>
                <Card className="p-6">
                  <CardHeader className="px-0 pt-0 mb-4">
                    <CardTitle className="flex items-center space-x-2">
                      <Sparkles size={20} />
                      <span>AI Suggestions</span>
                    </CardTitle>
                  </CardHeader>
                  <div className="space-y-3">
                    {atsScore.suggestions.map((suggestion, idx) => (
                      <div key={idx} className="p-3 bg-accent/5 border border-accent/20 rounded-lg flex items-start space-x-3">
                        <CheckCircle size={20} className="text-accent flex-shrink-0 mt-0.5" />
                        <p className="text-foreground text-sm">{suggestion}</p>
                      </div>
                    ))}
                  </div>
                </Card>
              </motion.div>
            )}

            {/* Job Matching Section */}
            <motion.div variants={itemVariants}>
              <Card className="p-6">
                <CardHeader className="px-0 pt-0 mb-4">
                  <CardTitle>Match with Job Description</CardTitle>
                  <CardDescription>Paste a job description to see how well your resume matches</CardDescription>
                </CardHeader>
                <textarea
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  placeholder="Paste the job description here..."
                  className="w-full h-32 p-3 border border-input rounded-lg bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-accent"
                />
                <Button
                  onClick={handleJobMatching}
                  disabled={!jobDescription.trim() || loading}
                  className="mt-4 rounded-lg"
                >
                  {loading ? (
                    <>
                      <LoadingSpinner size="sm" />
                      <span>Matching...</span>
                    </>
                  ) : (
                    'Analyze Match'
                  )}
                </Button>
              </Card>
            </motion.div>

            {/* Job Matching Results */}
            {jobMatching && (
              <motion.div
                variants={itemVariants}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <Card className="p-6">
                  <CardHeader className="px-0 pt-0 mb-6">
                    <CardTitle>Job Match Results</CardTitle>
                  </CardHeader>
                  <div className="space-y-6">
                    <div className="text-center p-6 bg-accent/5 rounded-lg border border-accent/20">
                      <p className="text-muted-foreground mb-2">Match Percentage</p>
                      <p className="text-5xl font-bold text-accent">{jobMatching.matchPercentage}%</p>
                    </div>

                    {jobMatching.matchedKeywords && jobMatching.matchedKeywords.length > 0 && (
                      <div>
                        <h3 className="font-semibold mb-3 text-green-500">Matched Keywords</h3>
                        <div className="flex flex-wrap gap-2">
                          {jobMatching.matchedKeywords.map((keyword) => (
                            <span key={keyword} className="px-3 py-1 bg-green-500/10 text-green-500 rounded-full text-sm border border-green-500/20">
                              {keyword}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {jobMatching.missingKeywords && jobMatching.missingKeywords.length > 0 && (
                      <div>
                        <h3 className="font-semibold mb-3 text-red-500">Missing Keywords</h3>
                        <div className="flex flex-wrap gap-2">
                          {jobMatching.missingKeywords.map((keyword) => (
                            <span key={keyword} className="px-3 py-1 bg-red-500/10 text-red-500 rounded-full text-sm border border-red-500/20">
                              {keyword}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {jobMatching.suggestions && jobMatching.suggestions.length > 0 && (
                      <div>
                        <h3 className="font-semibold mb-3">Recommendations</h3>
                        <div className="space-y-2">
                          {jobMatching.suggestions.map((suggestion, idx) => (
                            <div key={idx} className="p-3 bg-accent/5 border border-accent/20 rounded-lg flex items-start space-x-3">
                              <Sparkles size={18} className="text-accent flex-shrink-0 mt-0.5" />
                              <p className="text-foreground text-sm">{suggestion}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </Card>
              </motion.div>
            )}

            <motion.div variants={itemVariants}>
              <Button
                variant="outline"
                onClick={() => {
                  setStep('upload')
                  setSelectedFile(null)
                  setAtsScore(null)
                  setJobDescription('')
                  setJobMatching(null)
                }}
                className="w-full rounded-lg"
              >
                Analyze Another Resume
              </Button>
            </motion.div>
          </motion.div>
        )}
      </div>
    </motion.div>
  )
}

export default AnalyzerPage
