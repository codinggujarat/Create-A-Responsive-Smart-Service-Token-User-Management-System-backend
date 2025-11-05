# Smart Service Token & User Management System

## Overview
A comprehensive web application for managing service tokens and user information with automated email notifications and admin dashboard capabilities.

## Tech Stack
- **Backend**: Python Flask 3.x
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: React 18 with TailwindCSS
- **Authentication**: JWT-based admin authentication
- **Email**: Flask-Mail for notifications
- **Scheduling**: APScheduler for automated reminders
- **Export**: PDF (ReportLab), Excel/CSV (Pandas)

## Features
1. User submission form with auto-generated token numbers
2. Email confirmation on submission
3. Admin authentication and dashboard
4. Search and filter user data
5. Update work status (Pending/Completed)
6. Automated email reminders (Token #12, 15 min before service when 10 works completed)
7. Export data to PDF, Excel, CSV
8. Modern responsive UI with React and TailwindCSS

## Project Structure
```
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── config.py           # Configuration settings
│   ├── models.py           # Database models
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic
│   └── utils/              # Helper functions
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API calls
│   │   └── App.jsx         # Main app component
│   └── public/
├── requirements.txt        # Python dependencies
└── package.json           # Node.js dependencies

```

## Recent Changes
- 2025-11-04: ✅ Complete implementation of Smart Service Token & User Management System
  - Implemented Flask backend with SQLite database and SQLAlchemy ORM
  - Created REST API endpoints for user submission and admin operations
  - Built React frontend with TailwindCSS and responsive design
  - Integrated JWT authentication for admin panel
  - Configured APScheduler for automated email reminders
  - Added PDF, Excel, and CSV export functionality
  - Set up Flask-Mail for email confirmations and reminders
  - Application tested and verified working correctly

## User Preferences
- Modern, clean UI design
- Automated workflows
- Secure authentication
- Professional email notifications

## Architecture Decisions
- Using SQLite for simplicity and portability
- JWT for stateless authentication
- APScheduler for in-process task scheduling
- React Router for client-side routing
- TailwindCSS for utility-first styling
- Flask serves both API and built React frontend on port 5000
- Vite for modern frontend build tooling
- Email integration ready (requires SMTP configuration)

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt` and `npm install`
2. Build frontend: `npm run build`
3. Configure email settings in environment variables (optional)
4. Run application: `PYTHONPATH=/home/runner/workspace python backend/app.py`
5. Access at `http://localhost:5000`
6. Admin login: username=`admin`, password=`admin123` (change in production)

## Production Notes
- Configure SMTP settings for email functionality
- Change default admin credentials via environment variables
- Consider using Gunicorn or similar WSGI server for production
- Set up proper HTTPS/SSL certificates
- Configure CORS settings appropriately for production domain
