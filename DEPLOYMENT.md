# Deployment Guide

This guide explains how to deploy the Smart Service Token application with React frontend on Vercel and Flask backend on Render.

## Architecture Overview

```
┌─────────────────┐         ┌──────────────────┐
│   React Frontend │◄──API──►│   Flask Backend   │
│    (Vercel)      │         │     (Render)      │
└─────────────────┘         └──────────────────┘
                              │
                              ▼
                        SQLite Database
```

## Prerequisites

1. GitHub account
2. Vercel account
3. Render account

## Backend Deployment (Render)

### 1. Prepare Your Code

Ensure your code is pushed to a GitHub repository.

### 2. Create Web Service on Render

1. Go to https://dashboard.render.com
2. Click "New+" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - Name: `smart-service-token-backend`
   - Region: Choose the closest region
   - Branch: `main` (or your default branch)
   - Root Directory: Leave empty (root of repository)
   - Environment: `Python 3`

### 3. Configure Build and Start Commands

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn --bind 0.0.0.0:$PORT backend.app:app`

### 4. Set Environment Variables

Go to "Advanced" settings and add these environment variables:

```
SESSION_SECRET=your-random-session-secret
JWT_SECRET_KEY=your-random-jwt-secret
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-admin-password
```

### 5. Deploy

Click "Create Web Service". Render will automatically build and deploy your application.

## Frontend Deployment (Vercel)

### 1. Prepare Your Code

Ensure your code is pushed to a GitHub repository.

### 2. Create Project on Vercel

1. Go to https://vercel.com
2. Click "New Project"
3. Connect your GitHub repository
4. Import the project

### 3. Configure Project Settings

- Framework Preset: Vite
- Root Directory: Leave empty
- Build and Output Settings:
  - Build Command: `npm run build`
  - Output Directory: `frontend/dist`

### 4. Set Environment Variables

Add environment variables if needed:

```
VITE_API_URL=https://your-backend-url.onrender.com
```

If you don't set `VITE_API_URL`, the frontend will use `/api` as the base URL, which works if you're using Vercel's rewrite rules.

### 5. Deploy

Click "Deploy". Vercel will automatically build and deploy your application.

## Connecting Frontend and Backend

To make the frontend communicate with the backend, you have two options:

### Option 1: Using Environment Variables (Recommended)

Set the `VITE_API_URL` environment variable in Vercel to your Render backend URL:
```
VITE_API_URL=https://your-backend-url.onrender.com
```

### Option 2: Using Vercel Rewrites

The `vercel.json` file in your repository already includes rewrite rules to proxy API requests.

## Custom Domains (Optional)

### Frontend Domain

1. Go to your Vercel project
2. Click "Settings" → "Domains"
3. Add your domain
4. Follow the DNS configuration instructions

### Backend Domain

1. Go to your Render service
2. Click "Settings" → "Custom Domains"
3. Add your domain
4. Follow the DNS configuration instructions

## Monitoring and Logs

### Render (Backend)

1. Go to your Render service dashboard
2. Click "Logs" to view real-time logs
3. Set up alerts for error monitoring

### Vercel (Frontend)

1. Go to your Vercel project dashboard
2. Click "Analytics" for usage statistics
3. Check "Logs" for build and runtime logs

## Troubleshooting

### CORS Issues

If you encounter CORS issues, ensure your Flask backend has CORS enabled:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### Environment Variables Not Loading

Ensure all required environment variables are set in both Render and Vercel dashboards.

### Database Issues

The application uses SQLite, which is stored on Render's filesystem. Note that Render's free tier may have limitations on persistent storage.

## Scaling Considerations

For production use, consider:

1. Upgrading from SQLite to PostgreSQL
2. Adding a CDN for static assets
3. Implementing caching mechanisms
4. Setting up monitoring and alerting
5. Configuring auto-scaling options