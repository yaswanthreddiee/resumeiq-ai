import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Card, CardHeader, CardTitle, CardDescription } from '../components/Card'
import LoadingSpinner from '../components/LoadingSpinner'
import { pageVariants, containerVariants, itemVariants } from '../animations/pageTransitions'
import * as analyticsService from '../services/analyticsService'
import { Analytics } from '../types'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Area, AreaChart } from 'recharts'

const AnalyticsPage: React.FC = () => {
  const [analytics, setAnalytics] = useState<Analytics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true)
        const data = await analyticsService.getUserAnalytics()
        setAnalytics(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch analytics')
      } finally {
        setLoading(false)
      }
    }

    fetchAnalytics()
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
            <h1 className="text-4xl font-bold mb-2">Analytics</h1>
            <p className="text-muted-foreground">Track your resume improvement journey</p>
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

        {analytics && (
          <motion.div
            className="space-y-6"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            {/* Overview Cards */}
            <motion.div className="grid md:grid-cols-4 gap-6" variants={containerVariants}>
              {[
                { label: 'Total Resumes', value: analytics.totalResumes },
                { label: 'Average ATS Score', value: `${analytics.averageAtsScore.toFixed(1)}%` },
                { label: 'Total Analyses', value: analytics.totalAnalyses },
                { label: 'Analysis Rate', value: `${(analytics.totalAnalyses / analytics.totalResumes).toFixed(1) || 0}x` },
              ].map((stat) => (
                <motion.div key={stat.label} variants={itemVariants}>
                  <Card className="p-6">
                    <p className="text-muted-foreground text-sm font-medium">{stat.label}</p>
                    <p className="text-3xl font-bold mt-2">{stat.value}</p>
                  </Card>
                </motion.div>
              ))}
            </motion.div>

            {/* Charts */}
            <motion.div className="grid lg:grid-cols-2 gap-6" variants={containerVariants}>
              {/* ATS Score Trend */}
              <motion.div variants={itemVariants}>
                <Card className="p-6">
                  <CardHeader className="px-0 pt-0 mb-6">
                    <CardTitle>ATS Score Trend</CardTitle>
                    <CardDescription>Your average ATS score over time</CardDescription>
                  </CardHeader>
                  {analytics.scoreHistory && analytics.scoreHistory.length > 0 ? (
                    <ResponsiveContainer width="100%" height={300}>
                      <AreaChart data={analytics.scoreHistory}>
                        <defs>
                          <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="hsl(var(--accent))" stopOpacity={0.3} />
                            <stop offset="95%" stopColor="hsl(var(--accent))" stopOpacity={0} />
                          </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--muted))" />
                        <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" />
                        <YAxis stroke="hsl(var(--muted-foreground))" />
                        <Tooltip />
                        <Area type="monotone" dataKey="score" stroke="hsl(var(--accent))" fill="url(#colorScore)" />
                      </AreaChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="h-80 flex items-center justify-center text-muted-foreground">
                      No data available
                    </div>
                  )}
                </Card>
              </motion.div>

              {/* Upload Statistics */}
              <motion.div variants={itemVariants}>
                <Card className="p-6">
                  <CardHeader className="px-0 pt-0 mb-6">
                    <CardTitle>Upload Statistics</CardTitle>
                    <CardDescription>Number of uploads per day</CardDescription>
                  </CardHeader>
                  {analytics.uploadStats && analytics.uploadStats.length > 0 ? (
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={analytics.uploadStats}>
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--muted))" />
                        <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" />
                        <YAxis stroke="hsl(var(--muted-foreground))" />
                        <Tooltip />
                        <Bar dataKey="count" fill="hsl(var(--accent))" radius={[8, 8, 0, 0]} />
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
          </motion.div>
        )}
      </div>
    </motion.div>
  )
}

export default AnalyticsPage
