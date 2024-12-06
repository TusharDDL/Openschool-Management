# School Management System - File Structure

```
school-management/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   │   └── page.tsx           # Login page component
│   │   │   └── register/
│   │   │       └── page.tsx           # Registration page component
│   │   ├── dashboard/
│   │   │   ├── layout.tsx             # Dashboard layout
│   │   │   └── page.tsx               # Dashboard main page
│   │   ├── layout.tsx                 # Root layout
│   │   └── page.tsx                   # Home page
│   ├── components/
│   │   ├── ui/                        # Reusable UI components
│   │   └── forms/                     # Form components
│   ├── lib/
│   │   └── utils.ts                   # Utility functions
│   ├── providers/
│   │   └── auth-provider.tsx          # Authentication provider
│   ├── services/
│   │   ├── api.ts                     # API service
│   │   ├── auth.ts                    # Auth service
│   │   └── student.ts                 # Student service
│   └── types/
│       └── index.ts                   # TypeScript types
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/         # API endpoints
│   │   │       └── api.py             # API router
│   │   ├── core/
│   │   │   ├── config.py             # Configuration
│   │   │   ├── security.py           # Security utilities
│   │   │   └── database.py           # Database setup
│   │   └── models/                    # Database models
│   ├── migrations/                    # Database migrations
│   └── tests/                        # Backend tests
├── public/                           # Static files
├── docs/                            # Documentation
├── .env.example                     # Example environment variables
├── .env.local                       # Local environment variables
├── package.json                     # Frontend dependencies
└── requirements.txt                 # Backend dependencies
```