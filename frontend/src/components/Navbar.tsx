import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useTheme } from '../context/ThemeContext'
import { Button } from './Button'
import { Menu, X, Moon, Sun, LogOut, Settings } from 'lucide-react'
import { motion } from 'framer-motion'

const Navbar: React.FC = () => {
  const { isAuthenticated, logout, user } = useAuth()
  const { theme, toggleTheme } = useTheme()
  const [isOpen, setIsOpen] = useState(false)
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-card">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <div className="w-8 h-8 bg-gradient-to-br from-accent to-secondary rounded-lg group-hover:shadow-glow transition-shadow" />
            <span className="font-bold text-xl hidden sm:inline">ResumeIQ AI</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-6">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="text-foreground hover:text-accent transition">
                  Dashboard
                </Link>
                <Link to="/analyzer" className="text-foreground hover:text-accent transition">
                  Analyzer
                </Link>
                <Link to="/analytics" className="text-foreground hover:text-accent transition">
                  Analytics
                </Link>
                {user?.role === 'admin' && (
                  <Link to="/admin" className="text-foreground hover:text-accent transition">
                    Admin
                  </Link>
                )}
              </>
            ) : (
              <>
                <Link to="/" className="text-foreground hover:text-accent transition">
                  Home
                </Link>
              </>
            )}
          </div>

          {/* Right Section */}
          <div className="flex items-center space-x-4">
            {/* Theme Toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
              className="rounded-lg"
            >
              {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
            </Button>

            {/* Auth Buttons / User Menu */}
            {isAuthenticated ? (
              <div className="flex items-center space-x-2">
                <Link to="/settings">
                  <Button variant="ghost" size="icon" className="rounded-lg">
                    <Settings size={20} />
                  </Button>
                </Link>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleLogout}
                  className="rounded-lg flex items-center space-x-2"
                >
                  <LogOut size={16} />
                  <span className="hidden sm:inline">Logout</span>
                </Button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link to="/login">
                  <Button variant="outline" size="sm" className="rounded-lg">
                    Login
                  </Button>
                </Link>
                <Link to="/signup">
                  <Button size="sm" className="rounded-lg">
                    Sign Up
                  </Button>
                </Link>
              </div>
            )}

            {/* Mobile Menu Button */}
            <button
              className="md:hidden text-foreground"
              onClick={() => setIsOpen(!isOpen)}
            >
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="md:hidden pb-4 space-y-2"
          >
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="block px-4 py-2 hover:bg-muted rounded-lg">
                  Dashboard
                </Link>
                <Link to="/analyzer" className="block px-4 py-2 hover:bg-muted rounded-lg">
                  Analyzer
                </Link>
                <Link to="/analytics" className="block px-4 py-2 hover:bg-muted rounded-lg">
                  Analytics
                </Link>
                {user?.role === 'admin' && (
                  <Link to="/admin" className="block px-4 py-2 hover:bg-muted rounded-lg">
                    Admin
                  </Link>
                )}
              </>
            ) : (
              <Link to="/" className="block px-4 py-2 hover:bg-muted rounded-lg">
                Home
              </Link>
            )}
          </motion.div>
        )}
      </div>
    </nav>
  )
}

export default Navbar
