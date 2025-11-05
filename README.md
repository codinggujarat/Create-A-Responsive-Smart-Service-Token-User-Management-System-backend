# Smart Service Token & User Management System

A full-featured web application for managing service tokens with automated email notifications, admin dashboard, and data export capabilities.

## Features

### User Features
- **Service Request Form**: Submit service requests with name, email, address, contact number, and work description
- **Auto-Generated Token Numbers**: Sequential token numbers starting from 1
- **Email Confirmation**: Automatic email confirmation with token number and service details
- **Modern UI**: Clean, responsive design with TailwindCSS

### Admin Features
- **Secure Authentication**: JWT-based admin login system
- **Dashboard**: View all service requests with real-time statistics
- **Search & Filter**: Search by name, email, contact, or token number; filter by status
- **Status Management**: Update work status (Pending/Completed) directly from the dashboard
- **Data Export**: Export all data to PDF, Excel, or CSV formats
- **Automated Reminders**: System automatically sends reminder emails to Token #12 when 10 works are completed

### System Features
- **Automated Email System**: Flask-Mail integration for sending confirmations and reminders
- **Task Scheduler**: APScheduler running background jobs for automated reminders
- **SQLite Database**: Lightweight, file-based database with SQLAlchemy ORM
- **RESTful API**: Clean API endpoints for all operations

## Tech Stack

- **Backend**: Python 3.11, Flask 3.0
- **Frontend**: React 18, TailwindCSS 3.3
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-JWT-Extended
- **Email**: Flask-Mail
- **Scheduling**: APScheduler
- **Build Tool**: Vite 5
- **Data Export**: Pandas, ReportLab, OpenPyXL

## Installation

### Prerequisites
- Python 3.11+
- Node.js 20+

### Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Build the frontend**:
   ```bash
   npm run build
   ```

4. **Configure email settings** (optional):
   Create a `.env` file in the root directory:
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=noreply@yourdomain.com
   
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=admin123
   ```

5. **Run the application**:
   ```bash
   PYTHONPATH=/home/runner/workspace python backend/app.py
   ```

   The application will be available at `http://localhost:5000`

## Usage

### User Submission
1. Navigate to the home page
2. Fill in all required fields:
   - Full Name
   - Email Address
   - Contact Number
   - Address
   - Work Description
3. Click "Submit Request"
4. You'll receive a token number and a confirmation email

### Admin Access
1. Navigate to `/admin/login`
2. Login with credentials (default: `admin` / `admin123`)
3. View and manage all service requests
4. Update work status
5. Export data to PDF, Excel, or CSV

## API Endpoints

### User Endpoints
- `POST /api/submit` - Submit a new service request
- `GET /api/next-token` - Get the next available token number

### Admin Endpoints (Requires JWT Authentication)
- `POST /api/admin/login` - Admin login
- `GET /api/admin/users` - Get all users (supports search and filter)
- `PUT /api/admin/users/:id` - Update user status
- `GET /api/admin/stats` - Get statistics
- `GET /api/admin/export/excel` - Export to Excel
- `GET /api/admin/export/csv` - Export to CSV
- `GET /api/admin/export/pdf` - Export to PDF

## Database Schema

### Users Table
- `id` - Primary key
- `token_number` - Unique token number
- `name` - User's full name
- `email` - User's email address
- `address` - User's address
- `contact_number` - User's contact number
- `work_description` - Description of work needed
- `status` - Work status (Pending/Completed)
- `created_at` - Timestamp of creation
- `updated_at` - Timestamp of last update
- `reminder_sent` - Boolean flag for reminder status

### CompletedWork Table
- `id` - Primary key
- `count` - Number of completed works
- `last_updated` - Timestamp of last update

## Email Configuration

The system uses Flask-Mail for sending emails. To enable email functionality:

1. **Gmail**: Use an App Password (not your regular password)
   - Go to Google Account settings
   - Enable 2-factor authentication
   - Generate an App Password
   - Use this password in `MAIL_PASSWORD`

2. **Other SMTP Servers**: Update the configuration in `backend/config.py`

## Automated Reminders

The system includes an automated reminder feature:
- Runs every minute checking for conditions
- When 10 works are completed, sends a reminder to Token #12
- Reminder is sent 15 minutes before service time (configurable)
- Uses APScheduler for background task execution

## Development

### Frontend Development
```bash
npm run dev
```
This starts the Vite development server on port 5000 with hot module replacement.

### Backend Development
The Flask app runs in debug mode by default, which enables auto-reload on code changes.

## Deployment

### Deploying to Vercel (Frontend)

1. Push your code to a GitHub repository
2. Go to [Vercel](https://vercel.com) and create a new project
3. Connect your GitHub repository
4. Set environment variables if needed:
   - `VITE_API_URL`: Your backend API URL (e.g., https://your-api.onrender.com)
5. Vercel will automatically detect the Vite project and build it

### Deploying to Render (Backend)

1. Push your code to a GitHub repository
2. Go to [Render](https://render.com) and create a new web service
3. Connect your GitHub repository
4. Set the following configuration:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT backend.app:app`
5. Add environment variables:
   - `SESSION_SECRET`: A random secret key for sessions
   - `JWT_SECRET_KEY`: A random secret key for JWT tokens
   - `MAIL_SERVER`: Your SMTP server (e.g., smtp.gmail.com)
   - `MAIL_PORT`: Your SMTP port (e.g., 587)
   - `MAIL_USERNAME`: Your email username
   - `MAIL_PASSWORD`: Your email password or app password
   - `MAIL_DEFAULT_SENDER`: Your default sender email
   - `ADMIN_USERNAME`: Your admin username
   - `ADMIN_PASSWORD`: Your admin password

### CORS Configuration

The application is already configured to handle CORS. In production, you may want to restrict the origins to only your frontend domain.

### Environment Variables

Create a `.env` file in the root directory for local development:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@yourdomain.com

ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
SESSION_SECRET=your-session-secret
JWT_SECRET_KEY=your-jwt-secret
```

## Security Notes

- Change default admin credentials in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Configure CORS settings appropriately
- Use a production WSGI server (like Gunicorn) instead of Flask's development server

## Project Structure

```
├── backend/
│   ├── __init__.py
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Configuration settings
│   ├── models.py              # Database models
│   ├── routes/
│   │   ├── user_routes.py     # User API endpoints
│   │   └── admin_routes.py    # Admin API endpoints
│   ├── services/
│   │   └── scheduler_service.py  # Background scheduler
│   └── utils/
│       ├── email_service.py   # Email utilities
│       └── export_service.py  # Export utilities
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API service layer
│   │   ├── App.jsx            # Main app component
│   │   └── main.jsx           # Entry point
│   └── dist/                  # Built frontend (generated)
├── requirements.txt           # Python dependencies
├── package.json              # Node.js dependencies
├── vite.config.js            # Vite configuration
├── tailwind.config.js        # TailwindCSS configuration
└── README.md                 # This file
```

## License

MIT License - feel free to use this project for any purpose.

## Support

For issues, questions, or contributions, please contact the development team.
