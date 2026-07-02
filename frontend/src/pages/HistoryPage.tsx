import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Card, CardHeader, CardTitle, CardDescription } from '../components/Card'
import { Button } from '../components/Button'
import LoadingSpinner from '../components/LoadingSpinner'
import { pageVariants, containerVariants, itemVariants } from '../animations/pageTransitions'
import * as resumeService from '../services/resumeService'
import { Resume } from '../types'
import { Trash2, Eye, Download } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'

const HistoryPage: React.FC = () => {
  const [resumes, setResumes] = useState<Resume[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [deletingId, setDeletingId] = useState<string | null>(null)

  useEffect(() => {
    fetchResumes()
  }, [])

  const fetchResumes = async () => {
    try {
      setLoading(true)
      const data = await resumeService.getResumes()
      setResumes(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch resumes')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this resume?')) return

    try {
      setDeletingId(id)
      await resumeService.deleteResume(id)
      setResumes(resumes.filter(r => r.id !== id))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete resume')
    } finally {
      setDeletingId(null)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return (
    <motion.div
      initial="initial"
      animate="animate"
      exit="exit"
      variants={pageVariants}
      className="min-h-screen bg-background py-8 px-4"
    >
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          className="mb-8"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div variants={itemVariants}>
            <h1 className="text-4xl font-bold mb-2">Resume History</h1>
            <p className="text-muted-foreground">View and manage all your uploaded resumes</p>
          </motion.div>
        </motion.div>

        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6 p-4 bg-destructive/10 border border-destructive/50 rounded-lg text-destructive"
          >
            {error}
          </motion.div>
        )}

        {resumes.length > 0 ? (
          <motion.div
            className="space-y-4"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            {resumes.map((resume) => (
              <motion.div key={resume.id} variants={itemVariants}>
                <Card className="p-6 hover:border-accent/50 transition">
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                    <div className="mb-4 md:mb-0">
                      <h3 className="text-lg font-semibold">{resume.fileName}</h3>
                      <p className="text-muted-foreground text-sm">
                        Uploaded {formatDistanceToNow(new Date(resume.uploadedAt), { addSuffix: true })}
                      </p>
                      {resume.parsedContent && (
                        <div className="mt-2 flex flex-wrap gap-2">
                          {resume.parsedContent.skills && resume.parsedContent.skills.length > 0 && (
                            <span className="px-2 py-1 bg-accent/10 text-accent text-xs rounded">
                              {resume.parsedContent.skills.length} skills
                            </span>
                          )}
                          {resume.parsedContent.experience && resume.parsedContent.experience.length > 0 && (
                            <span className="px-2 py-1 bg-secondary/10 text-secondary text-xs rounded">
                              {resume.parsedContent.experience.length} experiences
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                    <div className="flex flex-col sm:flex-row gap-2">
                      {resume.atsScore && (
                        <div className="text-center p-3 bg-muted rounded-lg">
                          <p className="text-accent font-bold text-lg">{resume.atsScore.overallScore}%</p>
                          <p className="text-muted-foreground text-xs">ATS Score</p>
                        </div>
                      )}
                      <Button
                        variant="outline"
                        size="sm"
                        className="rounded-lg"
                        onClick={() => window.open(resume.fileUrl, '_blank')}
                      >
                        <Download size={16} />
                        <span className="hidden sm:inline ml-2">Download</span>
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        className="rounded-lg"
                        onClick={() => handleDelete(resume.id)}
                        disabled={deletingId === resume.id}
                      >
                        <Trash2 size={16} />
                        <span className="hidden sm:inline ml-2">Delete</span>
                      </Button>
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}
          </motion.div>
        ) : (
          <motion.div variants={itemVariants}>
            <Card className="p-12 text-center">
              <p className="text-muted-foreground mb-4">No resumes uploaded yet</p>
              <Button className="rounded-lg">
                Upload Your First Resume
              </Button>
            </Card>
          </motion.div>
        )}
      </div>
    </motion.div>
  )
}

export default HistoryPage
