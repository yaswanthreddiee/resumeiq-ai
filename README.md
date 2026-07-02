# ResumeIQ AI - Complete Production-Ready Resume Analyzer

<div align="center">

![ResumeIQ AI](https://img.shields.io/badge/ResumeIQ-AI%20Powered-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)

**An AI-powered SaaS application for intelligent resume analysis, ATS scoring, and job matching.**

[Features](#features) • [Tech Stack](#tech-stack) • [Getting Started](#getting-started) • [API Documentation](#api-documentation) • [Deployment](#deployment)

</div>

---

## Overview

ResumeIQ AI is a premium SaaS application that leverages artificial intelligence to provide comprehensive resume analysis. It offers ATS (Applicant Tracking System) compatibility scoring, intelligent job description matching, and AI-powered improvement suggestions.

Built with modern technologies and designed with production-grade architecture, ResumeIQ AI is ready to be deployed as a startup product.

---

## ✨ Features

### 🔐 Authentication & Security
- Secure user signup and login with JWT authentication
- Password hashing with bcrypt
- Protected routes and API endpoints
- Forgot password functionality
- Rate limiting and input validation
- CORS properly configured

### 📄 Resume Analysis
- **ATS Compatibility Analysis**: Evaluate resume performance in automated tracking systems
- **Resume Parsing**: Automatic extraction of skills, experience, education, projects, and certifications
- **Comprehensive Scoring Metrics**:
  - Overall ATS Score
  - Keyword Match Score
  - Grammar Score
  - Formatting Score
  - Action Verb Score
  - Section-by-Section Analysis

### 🎯 Job Matching
- Paste job descriptions and compare with resumes
- Calculate match percentages
- Identify matched and missing keywords
- AI-powered improvement suggestions
- Historical tracking of job matches

### 📊 Analytics & Dashboard
- Resume upload history and versioning
- ATS score trends over time
- Interactive analytics dashboards
- Resume improvement timeline
- Upload statistics
- Visual charts and graphs

### 👤 User Dashboard
- Personal profile management
- Analytics overview
- Recent resume activity
- Account settings
- Notification preferences

### 🛠️ Admin Dashboard
- User management and analytics
- System-wide statistics
- Report tracking
- Performance monitoring

---

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety and better DX
- **Vite** - Next-generation build tool
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **React Router v6** - Client-side routing
- **React Hook Form** - Efficient form handling
- **Shadcn UI** - High-quality component library
- **Recharts** - Interactive data visualization
- **Axios** - HTTP client
- **Lucide React** - Beautiful icons

### Backend
- **Python 3.11** - Server language
- **FastAPI** - Modern async web framework
- **MongoDB Atlas** - Cloud database
- **Motor** - Async MongoDB driver
- **Pydantic** - Data validation
- **JWT** - Secure authentication
- **OpenAI API** - AI/ML capabilities
- **bcrypt** - Password hashing
- **PyPDF2** - PDF parsing
- **python-docx** - DOCX parsing

### Infrastructure & Deployment
- **Docker** - Containerization
- **Docker Compose** - Local development
- **Vercel** - Frontend hosting
- **Render** - Backend hosting
- **MongoDB Atlas** - Database hosting

---

## 📋 Project Structure

```
resume-iq-ai/
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   ├── pages/               # Page components
│   │   ├── layouts/             # Layout components
│   │   ├── hooks/               # Custom React hooks
│   │   ├── context/             # React context
│   │   ├── services/            # API services
│   │   ├── types/               # TypeScript types
│   │   ├── utils/               # Utility functions
│   │   ├── animations/          # Framer Motion animations
│   │   ├── assets/              # Images and fonts
│   │   ├── styles/              # Global styles
│   │   └── App.tsx              # Main component
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── .env.example
│
├── backend/
│   ├── app/
│   │   ├── routers/             # API route handlers
│   │   ├── controllers/         # Business logic
│   │   ├── services/            # Service layer
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── middleware/          # Custom middleware
│   │   ├── database/            # Database config
│   │   ├── utils/               # Utilities
│   │   ├── config.py            # Configuration
│   │   └── main.py              # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── docker-compose.yml
│
├── docker-compose.yml           # Multi-container setup
├── .env.example                 # Environment template
└── README.md                    # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- MongoDB Atlas account
- OpenAI API key
- Docker (optional)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resumeiq-ai.git
   cd resumeiq-ai
   ```

2. **Setup environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up
   ```

   - Frontend: http://localhost:5173
   - Backend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Manual Setup

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Backend runs on `http://localhost:8000`

---

## 📡 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main API Endpoints

#### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password

#### Resumes
- `POST /api/resumes/upload` - Upload resume
- `GET /api/resumes` - Get all resumes
- `GET /api/resumes/{resume_id}` - Get specific resume
- `DELETE /api/resumes/{resume_id}` - Delete resume
- `POST /api/resumes/{resume_id}/analyze-ats` - Analyze ATS
- `POST /api/resumes/{resume_id}/match-job` - Match with job description
- `GET /api/resumes/{resume_id}/ats-score` - Get ATS score

#### Analytics
- `GET /api/analytics` - Get user analytics
- `GET /api/analytics/admin/analytics` - Get admin analytics

---

## 🔐 Security Considerations

- ✅ All passwords hashed with bcrypt
- ✅ JWT tokens for stateless authentication
- ✅ Input validation on all endpoints
- ✅ Rate limiting to prevent abuse
- ✅ CORS properly configured
- ✅ Environment variables for sensitive data
- ✅ Secure file upload handling
- ✅ NoSQL injection prevention with MongoDB
- ✅ HTTPS enforced in production

---

## ⚡ Performance Optimizations

- Database indexing on frequently queried fields
- Async/await for non-blocking operations
- Pagination for large datasets
- Lazy loading of frontend components
- Code splitting and tree shaking
- Efficient state management
- Caching strategies
- CDN for static assets

---

## 🌐 Deployment

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Set environment variables
3. Vercel auto-deploys on push to main

```bash
# Manual build
cd frontend
npm run build
vercel deploy --prod
```

### Backend (Render)

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure build command: `pip install -r backend/requirements.txt`
4. Configure start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Add environment variables
6. Deploy

### Database (MongoDB Atlas)

1. Create cluster on MongoDB Atlas
2. Configure network access
3. Create database and collections
4. Set connection string in environment variables

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## 📈 Monitoring & Analytics

- User activity tracking
- Error logging and reporting
- Performance monitoring
- API usage analytics
- Resume analysis patterns

---

## 🗺️ Roadmap

- [ ] Multi-language resume support
- [ ] Advanced AI suggestions using GPT-4
- [ ] Resume template suggestions
- [ ] Job board integration
- [ ] Collaborative resume reviews
- [ ] LinkedIn profile analysis
- [ ] Resume scoring benchmarks
- [ ] Email notifications
- [ ] API for third-party integrations
- [ ] Mobile application
- [ ] Real-time collaboration
- [ ] Advanced analytics

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 Development Guidelines

### Code Style
- Follow TypeScript best practices
- Use meaningful variable names
- Keep components small and focused
- Use React hooks for state management
- Implement proper error handling
- Write maintainable, modular code

### Commit Messages
- Use conventional commits
- Format: `type(scope): description`
- Examples: `feat(auth): add JWT validation`, `fix(resume): parse PDF correctly`

### Branch Naming
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation
- `refactor/` for refactoring

---

## 🐛 Known Issues

- None currently

---

## 📧 Support & Contact

For issues, feature requests, or questions:
- Open an issue on GitHub
- Email: support@resumeiq.com
- Documentation: https://docs.resumeiq.com

---

## 📄 License

Proprietary - All rights reserved

---

## 👤 Author

**Yaswanth Reddie**
- GitHub: [@yaswanthreddiee](https://github.com/yaswanthreddiee)
- Email: yaswanth@example.com

---

<div align="center">

Made with ❤️ by Yaswanth Reddie

[⬆ back to top](#resumeiq-ai---complete-production-ready-resume-analyzer)

</div>
