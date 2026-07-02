import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { ArrowRight, CheckCircle, Zap, BarChart3, Brain, Shield, Sparkles } from 'lucide-react'
import { Button } from '../components/Button'
import GradientText from '../components/GradientText'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import { pageVariants, containerVariants, itemVariants } from '../animations/pageTransitions'

const HomePage: React.FC = () => {
  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Analysis',
      description: 'Advanced AI algorithms analyze your resume comprehensively',
    },
    {
      icon: Zap,
      title: 'ATS Optimization',
      description: 'Get optimized for Applicant Tracking Systems',
    },
    {
      icon: BarChart3,
      title: 'Detailed Analytics',
      description: 'Track your resume performance over time',
    },
    {
      icon: Sparkles,
      title: 'Smart Suggestions',
      description: 'AI-powered improvement recommendations',
    },
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Your data is encrypted and secure',
    },
    {
      icon: CheckCircle,
      title: 'Job Matching',
      description: 'Match your resume with job descriptions',
    },
  ]

  return (
    <motion.div
      initial="initial"
      animate="animate"
      exit="exit"
      variants={pageVariants}
      className="min-h-screen bg-background"
    >
      <Navbar />

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-4 overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            className="absolute -top-40 -right-40 w-80 h-80 bg-accent/10 rounded-full blur-3xl"
            animate={{ x: [0, 50, 0], y: [0, 30, 0] }}
            transition={{ duration: 8, repeat: Infinity }}
          />
          <motion.div
            className="absolute top-1/2 -left-40 w-80 h-80 bg-secondary/10 rounded-full blur-3xl"
            animate={{ x: [0, -50, 0], y: [0, -30, 0] }}
            transition={{ duration: 10, repeat: Infinity }}
          />
        </div>

        <motion.div
          className="relative max-w-4xl mx-auto text-center"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div variants={itemVariants} className="mb-6">
            <span className="inline-block px-4 py-2 rounded-full bg-accent/10 text-accent border border-accent/20 text-sm font-medium">
              ✨ AI-Powered Resume Analyzer
            </span>
          </motion.div>

          <motion.h1 variants={itemVariants} className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
            Your Resume,
            <br />
            <GradientText>Optimized by AI</GradientText>
          </motion.h1>

          <motion.p variants={itemVariants} className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Analyze your resume with AI, get ATS scores, compare with job descriptions, and receive intelligent
            suggestions to land your dream job.
          </motion.p>

          <motion.div variants={itemVariants} className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/signup">
              <Button size="lg" className="rounded-lg flex items-center space-x-2">
                <span>Get Started Free</span>
                <ArrowRight size={20} />
              </Button>
            </Link>
            <Link to="/login">
              <Button variant="outline" size="lg" className="rounded-lg">
                Sign In
              </Button>
            </Link>
          </motion.div>
        </motion.div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 bg-muted/30">
        <div className="max-w-6xl mx-auto">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Powerful Features for Your Success
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Everything you need to optimize your resume and land your dream job.
            </p>
          </motion.div>

          <motion.div
            className="grid md:grid-cols-3 gap-8"
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
          >
            {features.map((feature) => {
              const Icon = feature.icon
              return (
                <motion.div
                  key={feature.title}
                  variants={itemVariants}
                  className="p-6 rounded-lg border border-card bg-card/30 hover:bg-card/50 hover:border-accent/50 transition group"
                  whileHover={{ y: -5 }}
                >
                  <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center mb-4 group-hover:bg-accent group-hover:text-background transition">
                    <Icon size={24} />
                  </div>
                  <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.description}</p>
                </motion.div>
              )
            })}
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <motion.div
          className="max-w-4xl mx-auto bg-gradient-to-r from-accent/10 to-secondary/10 border border-accent/20 rounded-2xl p-12 text-center"
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Optimize Your Resume?
          </h2>
          <p className="text-muted-foreground mb-8 max-w-2xl mx-auto">
            Join thousands of job seekers who have improved their resumes with ResumeIQ AI.
          </p>
          <Link to="/signup">
            <Button size="lg" className="rounded-lg">
              Start Free Trial
            </Button>
          </Link>
        </motion.div>
      </section>

      <Footer />
    </motion.div>
  )
}

export default HomePage
