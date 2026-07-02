import { useAuth } from '../context/AuthContext'
import { Navigate } from 'react-router-dom'

interface ProtectedRouteProps {
  children: React.ReactNode
  admin?: boolean
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, admin = false }) => {
  const { isAuthenticated, loading, user } = useAuth()

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin">
          <div className="w-12 h-12 border-4 border-accent border-t-transparent rounded-full" />
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (admin && user?.role !== 'admin') {
    return <Navigate to="/dashboard" replace />
  }

  return <>{children}</>
}

export default ProtectedRoute
