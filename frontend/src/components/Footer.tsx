import { Link } from 'react-router-dom'
import { Github, Twitter, Linkedin, Mail } from 'lucide-react'

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-muted border-t border-card mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-accent to-secondary rounded-lg" />
              <span className="font-bold">ResumeIQ AI</span>
            </div>
            <p className="text-muted-foreground text-sm">
              AI-powered resume analyzer with ATS scoring and job matching.
            </p>
          </div>

          {/* Product */}
          <div>
            <h3 className="font-semibold mb-4">Product</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link to="/#features" className="hover:text-accent transition">
                  Features
                </Link>
              </li>
              <li>
                <Link to="/#pricing" className="hover:text-accent transition">
                  Pricing
                </Link>
              </li>
              <li>
                <Link to="/" className="hover:text-accent transition">
                  Security
                </Link>
              </li>
            </ul>
          </div>

          {/* Company */}
          <div>
            <h3 className="font-semibold mb-4">Company</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link to="/" className="hover:text-accent transition">
                  Blog
                </Link>
              </li>
              <li>
                <Link to="/" className="hover:text-accent transition">
                  Careers
                </Link>
              </li>
              <li>
                <Link to="/" className="hover:text-accent transition">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Social */}
          <div>
            <h3 className="font-semibold mb-4">Follow Us</h3>
            <div className="flex space-x-4">
              <a href="#" className="text-muted-foreground hover:text-accent transition">
                <Github size={20} />
              </a>
              <a href="#" className="text-muted-foreground hover:text-accent transition">
                <Twitter size={20} />
              </a>
              <a href="#" className="text-muted-foreground hover:text-accent transition">
                <Linkedin size={20} />
              </a>
              <a href="#" className="text-muted-foreground hover:text-accent transition">
                <Mail size={20} />
              </a>
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div className="border-t border-card pt-8 flex flex-col md:flex-row justify-between items-center text-sm text-muted-foreground">
          <p>&copy; {currentYear} ResumeIQ AI. All rights reserved.</p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <Link to="/" className="hover:text-accent transition">
              Privacy Policy
            </Link>
            <Link to="/" className="hover:text-accent transition">
              Terms of Service
            </Link>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
