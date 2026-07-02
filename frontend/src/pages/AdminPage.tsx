import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Card, CardHeader, CardTitle, CardDescription } from '../components/Card'
import LoadingSpinner from '../components/LoadingSpinner'
import { pageVariants, containerVariants, itemVariants } from '../animations/pageTransitions'
import * as analyticsService from '../services/analyticsService'
import { AdminStats } from '../types'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import { Users, FileText, BarChart3, Zap } from 'lucide-react'

const AdminPage: React.FC = () => {
  const [stats, setStats] = useState<AdminStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true)
        const data = await analyticsService.getAdminAnalytics()
        setStats(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch admin stats')
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
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
            <h1 className="text-4xl font-bold mb-2">Admin Dashboard</h1>
            <p className="text-muted-foreground">System overview and analytics</p>
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

        {stats && (
          <motion.div
            className="space-y-6"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            {/* Overview Cards */}
            <motion.div className="grid md:grid-cols-4 gap-6" variants={containerVariants}>
              {[
                { icon: Users, label: 'Total Users', value: stats.totalUsers, color: 'text-accent' },
                { icon: FileText, label: 'Total Resumes', value: stats.totalResumes, color: 'text-secondary' },
                { icon: BarChart3, label: 'Total Analyses', value: stats.totalAnalyses, color: 'text-accent' },
                { icon: Zap, label: 'Avg ATS Score', value: `${stats.averageAtsScore.toFixed(1)}%`, color: 'text-accent' },
              ].map((stat) => {
                const Icon = stat.icon
                return (
                  <motion.div key={stat.label} variants={itemVariants}>
                    <Card className="p-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-muted-foreground text-sm font-medium">{stat.label}</p>
                          <p className="text-3xl font-bold mt-2">{stat.value}</p>
                        </div>
                        <Icon className={`w-12 h-12 ${stat.color}/30`} />
                      </div>
                    </Card>
                  </motion.div>
                )
              })}
            </motion.div>

            {/* User Growth Chart */}
            <motion.div variants={itemVariants}>
              <Card className="p-6">
                <CardHeader className="px-0 pt-0 mb-6">
                  <CardTitle>User Growth</CardTitle>
                  <CardDescription>New users over time</CardDescription>
                </CardHeader>
                {stats.userGrowth && stats.userGrowth.length > 0 ? (
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={stats.userGrowth}>
                      <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--muted))" />
                      <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" />
                      <YAxis stroke="hsl(var(--muted-foreground))" />
                      <Tooltip />
                      <Line type="monotone" dataKey="users" stroke="hsl(var(--accent))" />
                    </LineChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="h-80 flex items-center justify-center text-muted-foreground">
                    No data available
                  </div>
                )}
              </Card>
            </motion.div>
          </motion.div>
        )}
      </div>
    </motion.div>
  )
}

export default AdminPage
