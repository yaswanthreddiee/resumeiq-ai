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
import { Mail, Lock, User, AlertCircle } from 'lucide-react'

const SignupPage: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { signup } = useAuth()
  const navigate = useNavigate()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setError(null)
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }))
  }

  const validateForm = () => {
    if (!formData.name.trim()) return 'Name is required'
    if (!formData.email.includes('@')) return 'Valid email is required'
    if (formData.password.length < 8) return 'Password must be at least 8 characters'
    if (formData.password !== formData.confirmPassword) return 'Passwords do not match'
    return null
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const validationError = validateForm()
    if (validationError) {
      setError(validationError)
      return
    }

    setLoading(true)
    try {
      await signup(formData.email, formData.password, formData.name)
      navigate('/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Signup failed')
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
                  Create <GradientText>Account</GradientText>
                </h1>
                <p className="text-muted-foreground">
                  Join ResumeIQ AI and optimize your resume
                </p>
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
                  <label className="block text-sm font-medium mb-2">Full Name</label>
                  <div className="relative">
                    <User className="absolute left-3 top-3 text-muted-foreground" size={18} />
                    <Input
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      placeholder="John Doe"
                      className="pl-10"
                      disabled={loading}
                    />
                  </div>
                </div>

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
                      placeholder="At least 8 characters"
                      className="pl-10"
                      disabled={loading}
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Confirm Password</label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 text-muted-foreground" size={18} />
                    <Input
                      type="password"
                      name="confirmPassword"
                      value={formData.confirmPassword}
                      onChange={handleChange}
                      placeholder="Confirm password"
                      className="pl-10"
                      disabled={loading}
                    />
                  </div>
                </div>

                <Button
                  type="submit"
                  className="w-full rounded-lg mt-6 flex items-center justify-center space-x-2"
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <LoadingSpinner size="sm" />
                      <span>Creating account...</span>
                    </>
                  ) : (
                    <span>Sign Up</span>
                  )}
                </Button>
              </form>

              <p className="text-center text-muted-foreground text-sm mt-6">
                Already have an account?{' '}
                <Link to="/login" className="text-accent hover:underline font-medium">
                  Sign in
                </Link>
              </p>
            </Card>
          </motion.div>
        </div>
      </div>
    </motion.div>
  )
}

export default SignupPage
