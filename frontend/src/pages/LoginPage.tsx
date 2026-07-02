import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth } from '../context/AuthContext'
import { Button } from '../components/Button'
import { Input } from '../components/Input'
import { Card } from '../components/Card'
import Navbar from '../components/Navbar'
import GradientText from '../components/GradientText'
import LoadingSpinner from '../components/LoadingSpinner'
import { pageVariants } from '../animations/pageTransitions'
import { Mail, Lock, AlertCircle } from 'lucide-react'

const LoginPage: React.FC = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setError(null)
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.email || !formData.password) {
      setError('Email and password are required')
      return
    }

    setLoading(true)
    try {
      await login(formData.email, formData.password)
      navigate('/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
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
      className="min-h-screen bg-background"
    >
      <Navbar />
      <div className="pt-24 pb-12 px-4">
        <div className="max-w-md mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card className="p-8">
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold mb-2">
                  Welcome <GradientText>Back</GradientText>
                </h1>
                <p className="text-muted-foreground">Sign in to your account</p>
              </div>

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

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Email</label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 text-muted-foreground" size={18} />
                    <Input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="you@example.com"
                      className="pl-10"
                      disabled={loading}
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Password</label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 text-muted-foreground" size={18} />
                    <Input
                      type="password"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      placeholder="Enter your password"
                      className="pl-10"
                      disabled={loading}
                    />
                  </div>
                </div>

                <div className="flex items-center justify-between text-sm">
                  <label className="flex items-center space-x-2 cursor-pointer">
                    <input type="checkbox" className="rounded" />
                    <span>Remember me</span>
                  </label>
                  <Link to="#" className="text-accent hover:underline">
                    Forgot password?
                  </Link>
                </div>

                <Button
                  type="submit"
                  className="w-full rounded-lg mt-6 flex items-center justify-center space-x-2"
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <LoadingSpinner size="sm" />
                      <span>Signing in...</span>
                    </>
                  ) : (
                    <span>Sign In</span>
                  )}
                </Button>
              </form>

              <p className="text-center text-muted-foreground text-sm mt-6">
                Don't have an account?{' '}
                <Link to="/signup" className="text-accent hover:underline font-medium">
                  Sign up
                </Link>
              </p>
            </Card>
          </motion.div>
        </div>
      </div>
    </motion.div>
  )
}

export default LoginPage
