# ResumeIQ AI - Production-Ready Resume Analyzer

## Overview

ResumeIQ AI is a premium SaaS application that leverages artificial intelligence to analyze resumes, provide ATS (Applicant Tracking System) scoring, and offer intelligent job matching with AI-powered improvement suggestions.

## Key Features

### Authentication & Security
- Secure user signup and login with JWT authentication
- Password hashing with bcrypt
- Forgot password functionality
- Protected routes and API endpoints
- Rate limiting and input validation

### Resume Analysis
- **ATS Compatibility Analysis**: Evaluate how well your resume performs in automated tracking systems
- **Resume Parsing**: Extract skills, experience, education, projects, and certifications
- **Scoring Metrics**:
  - Overall ATS Score
  - Keyword Match
  - Grammar Score
  - Formatting Score
  - Action Verb Score
  - Section Analysis

### Job Matching
- Paste job descriptions and compare with resumes
- Generate match percentages
- Identify missing keywords
- AI-powered improvement suggestions

### Analytics & History
- Resume upload history and versioning
- ATS score trends and visualization
- Interactive analytics dashboards
- Resume improvement timeline
- Previous analysis reports

### Admin Dashboard
- User management
- System analytics
- Report tracking

## Technology Stack

### Frontend
- **React** (Vite) - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **React Router** - Navigation
- **React Hook Form** - Form management
- **Shadcn UI** - Component library
- **Recharts** - Data visualization
- **Axios** - HTTP client

### Backend
- **Python** - Server language
- **FastAPI** - Web framework
- **MongoDB Atlas** - Database
- **Pydantic** - Data validation
- **JWT** - Authentication
- **OpenAI API** - AI/ML capabilities

### Infrastructure
- **Frontend**: Vercel
- **Backend**: Render
- **Database**: MongoDB Atlas

## Project Structure

```
resume-iq-ai/
├── frontend/              # React Vite application
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Page components
│   │   ├── layouts/      # Layout components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── context/      # React context
│   │   ├── services/     # API services
│   │   ├── assets/       # Images, fonts, etc.
│   │   ├── animations/   # Framer Motion animations
│   │   ├── types/        # TypeScript types
│   │   ├── utils/        # Utility functions
│   │   └── App.tsx       # Main app component
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── routers/      # API routes
│   │   ├── controllers/  # Business logic
│   │   ├── services/     # Service layer
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── middleware/   # Custom middleware
│   │   ├── database/     # Database config
│   │   ├── utils/        # Utility functions
│   │   ├── config.py     # Configuration
│   │   └── main.py       # FastAPI app
│   ├── requirements.txt
│   ├── .env.example
│   └── docker-compose.yml
│
├── .env.example          # Environment variables template
├── docker-compose.yml    # Docker configuration
└── README.md            # This file
```

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- MongoDB Atlas account
- OpenAI API key

### Environment Setup

1. Clone the repository
```bash
git clone https://github.com/yaswanthreddiee/resumeiq-ai.git
cd resumeiq-ai
```

2. Create `.env` file from `.env.example`
```bash
cp .env.example .env
```

3. Fill in required environment variables

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Backend runs on `http://localhost:8000`

## API Documentation

Once backend is running, visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## Features in Detail

### Authentication Flow
1. User signs up with email and password
2. Password is hashed with bcrypt
3. JWT token issued on login
4. Token used for subsequent API requests
5. Protected routes check token validity

### Resume Analysis Pipeline
1. User uploads resume (PDF/DOCX)
2. Backend parses resume content
3. Extract sections: skills, experience, education, etc.
4. Generate ATS score based on multiple metrics
5. Query OpenAI for improvement suggestions
6. Store analysis in database
7. Display results with visualizations

### Job Matching Process
1. User pastes job description
2. Backend analyzes job requirements
3. Compare with user's resume
4. Calculate match percentage
5. Identify missing keywords
6. Generate AI suggestions for improvement

### Analytics
- Track ATS scores over time
- Monitor resume improvement progress
- Visualize upload statistics
- Interactive charts and graphs

## Security Considerations

- All passwords hashed with bcrypt
- JWT tokens for stateless authentication
- Input validation on all endpoints
- Rate limiting to prevent abuse
- CORS properly configured
- Environment variables for sensitive data
- Secure file upload handling
- SQL injection prevention with MongoDB

## Performance Optimizations

- Database indexing on frequently queried fields
- Caching strategies for API responses
- Pagination for large datasets
- Lazy loading of components
- Code splitting in frontend
- Efficient state management

## Deployment

### Frontend (Vercel)
```bash
cd frontend
npm run build
# Push to GitHub, Vercel auto-deploys
```

### Backend (Render)
```bash
# Push to GitHub
# Connect to Render
# Set environment variables
# Deploy
```

### Database (MongoDB Atlas)
- Create cluster on MongoDB Atlas
- Configure network access
- Create database and collections
- Set connection string in environment

## Development Best Practices

- Follow TypeScript best practices in frontend
- Use clean architecture in backend
- Implement comprehensive error handling
- Write maintainable, modular code
- Follow REST API standards
- Use meaningful variable and function names
- Keep components small and focused
- Use React hooks for state management
- Implement proper logging

## Testing

- Unit tests for utility functions
- Integration tests for API endpoints
- Component tests for React components
- E2E tests for critical user flows

## Monitoring & Analytics

- User activity tracking
- Error logging and reporting
- Performance monitoring
- API usage analytics

## Roadmap

- [ ] Multi-language resume support
- [ ] Advanced AI suggestions using GPT-4
- [ ] Resume template suggestions
- [ ] Job board integration
- [ ] Collaborative resume reviews
- [ ] LinkedIn profile analysis
- [ ] Resume scoring benchmarks
- [ ] Email notifications
- [ ] API for third-party integrations

## Support & Contact

For issues, feature requests, or questions, please open an issue on GitHub.

## License

Proprietary - All rights reserved

## Contributors

Yaswanth Reddie
