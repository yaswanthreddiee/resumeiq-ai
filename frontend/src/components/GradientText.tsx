interface GradientTextProps {
  children: React.ReactNode
  className?: string
}

const GradientText: React.FC<GradientTextProps> = ({ children, className = '' }) => {
  return (
    <span className={`bg-gradient-to-r from-accent via-secondary to-accent bg-clip-text text-transparent ${className}`}>
      {children}
    </span>
  )
}

export default GradientText
