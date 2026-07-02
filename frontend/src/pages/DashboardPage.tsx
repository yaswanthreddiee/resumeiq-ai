import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useAuth } from '../context/AuthContext'
import { Card, CardHeader, CardTitle, CardDescription, CardFooter } from '../components/Card'
import { Button } from '../components/Button'
import LoadingSpinner from '../components/LoadingSpinner'
import { pageVariants, containerVariants, itemVariants } from '../animations/pageTransitions'
import * as analyticsService from '../services/analyticsService'
import * as resumeService from '../services/resumeService'
import { Analytics, Resume } from '../types'
import { FileUp, BarChart3, Clock, Plus } from 'lucide-react'
import { Link } from 'react-router-dom'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'

const DashboardPage: React.FC = () => {
  const { user } = useAuth()
  const [analytics, setAnalytics] = useState<Analytics | null>(null)
  const [resumes, setResumes] = useState<Resume[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const [analyticsData, resumesData] = await Promise.all([
          analyticsService.getUserAnalytics(),
          resumeService.getResumes(),
        ])
        setAnalytics(analyticsData)
        setResumes(resumesData.slice(0, 5)) // Show latest 5
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch data')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

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
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          className="mb-8"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div variants={itemVariants}>
            <h1 className="text-4xl font-bold mb-2">
              Welcome back, <span className="text-accent">{user?.name}</span>
            </h1>
            <p className="text-muted-foreground">Here's your resume analysis overview</p>
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

        {/* Stats */}
        <motion.div
          className="grid md:grid-cols-4 gap-6 mb-8"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div variants={itemVariants}>
            <Card className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-muted-foreground text-sm font-medium">Total Resumes</p>
                  <p className="text-3xl font-bold mt-2">{analytics?.totalResumes || 0}</p>
                </div>
                <FileUp className="w-12 h-12 text-accent/30" />
              </div>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Card className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-muted-foreground text-sm font-medium">Average ATS Score</p>
                  <p className="text-3xl font-bold mt-2">{analytics?.averageAtsScore?.toFixed(1) || 0}%</p>
                </div>
                <BarChart3 className="w-12 h-12 text-secondary/30" />
              </div>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Card className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-muted-foreground text-sm font-medium">Total Analyses</p>
                  <p className="text-3xl font-bold mt-2">{analytics?.totalAnalyses || 0}</p>
                </div>
                <Clock className="w-12 h-12 text-accent/30" />
              </div>
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Link to="/analyzer">
              <Card className="p-6 cursor-pointer hover:border-accent/50 transition">
                <div className="flex items-center justify-between h-full">
                  <div>
                    <p className="text-muted-foreground text-sm font-medium">New Analysis</p>
                    <Button className="mt-2 text-sm" size="sm">
                      Start Now
                    </Button>
                  </div>
                  <Plus className="w-12 h-12 text-accent/30" />
                </div>
              </Card>
            </Link>
          </motion.div>
        </motion.div>

        {/* Charts */}
        <motion.div
          className="grid lg:grid-cols-2 gap-6 mb-8"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div variants={itemVariants}>
            <Card className="p-6">
              <CardHeader className="px-0 pt-0">
                <CardTitle>ATS Score Trend</CardTitle>
                <CardDescription>Your average ATS score over time</CardDescription>
              </CardHeader>
              {analytics?.scoreHistory && analytics.scoreHistory.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={analytics.scoreHistory}>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--muted))" />
                    <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" />
                    <YAxis stroke="hsl(var(--muted-foreground))" />
                    <Tooltip />
                    <Line type="monotone" dataKey="score" stroke="hsl(var(--accent))" />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-80 flex items-center justify-center text-muted-foreground">
                  No data available
                </div>
              )}
            </Card>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Card className="p-6">
              <CardHeader className="px-0 pt-0">
                <CardTitle>Upload Statistics</CardTitle>
                <CardDescription>Number of uploads per day</CardDescription>
              </CardHeader>
              {analytics?.uploadStats && analytics.uploadStats.length > 0 ? (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={analytics.uploadStats}>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--muted))" />
                    <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" />
                    <YAxis stroke="hsl(var(--muted-foreground))" />
                    <Tooltip />
                    <Bar dataKey="count" fill="hsl(var(--accent))" />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-80 flex items-center justify-center text-muted-foreground">
                  No data available
                </div>
              )}
            </Card>
          </motion.div>
        </motion.div>

        {/* Recent Resumes */}
        <motion.div variants={itemVariants}>
          <Card className="p-6">
            <CardHeader className="px-0 pt-0">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Recent Resumes</CardTitle>
                  <CardDescription>Your latest uploads</CardDescription>
                </div>
                <Link to="/history">
                  <Button variant="outline" size="sm" className="rounded-lg">
                    View All
                  </Button>
                </Link>
              </div>
            </CardHeader>
            {resumes.length > 0 ? (
              <div className="space-y-4 mt-6">
                {resumes.map((resume) => (
                  <div key={resume.id} className="p-4 border border-card rounded-lg hover:border-accent/50 transition">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium">{resume.fileName}</p>
                        <p className="text-sm text-muted-foreground">
                          {new Date(resume.uploadedAt).toLocaleDateString()}
                        </p>
                      </div>
                      {resume.atsScore && (
                        <div className="text-right">
                          <p className="text-lg font-bold text-accent">{resume.atsScore.overallScore}%</p>
                          <p className="text-xs text-muted-foreground">ATS Score</p>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                <p>No resumes uploaded yet</p>
                <Link to="/analyzer">
                  <Button variant="outline" size="sm" className="mt-4 rounded-lg">
                    Upload Resume
                  </Button>
                </Link>
              </div>
            )}
          </Card>
        </motion.div>
      </div>
    </motion.div>
  )
}

export default DashboardPage
