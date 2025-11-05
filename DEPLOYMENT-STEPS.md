# Complete Deployment Steps

This guide provides detailed step-by-step instructions to deploy your Smart Service Token application with React frontend on Vercel and Flask backend on Render.

## Prerequisites

1. GitHub account
2. Vercel account (free)
3. Render account (free)
4. Your application code ready in a local repository

## Step 1: Prepare Your Code Repository

1. Make sure your project structure looks like this:
   ```
   SmartServiceToken-2/
   ├── backend/
   ├── frontend/
   ├── requirements.txt
   ├── package.json
   └── ...other files
   ```

2. Initialize git repository (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. Create a new repository on GitHub and push your code:
   ```bash
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy Backend to Render

1. Go to [Render Dashboard](https://dashboard.render.com)

2. Click "New+" → "Web Service"

3. Connect your GitHub account and select your repository

4. Configure the service with these settings:
   - Name: `smart-service-token-backend`
   - Region: Choose the closest region to your users
   - Branch: `main`
   - Root Directory: Leave empty (root of repository)
   - Environment: `Python 3`

5. Configure Build and Start commands:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT backend.app:app`

6. Go to "Advanced" settings and add these environment variables:
   ```
   SESSION_SECRET=your-random-secret-key-here
   JWT_SECRET_KEY=your-random-jwt-key-here
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=noreply@yourdomain.com
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=your-secure-admin-password
   ```

7. Click "Create Web Service"

8. Wait for deployment to complete (this may take 5-10 minutes)

9. Once deployed, note your backend URL which will look like:
   `https://smart-service-token-backend.onrender.com`

## Step 3: Update Frontend Configuration (Optional)

For local development, you can create a [.env.local](file:///c%3A/Users%5C91704%5CDownloads%5CSmartServiceToken-2/.env.local) file in the frontend directory with:
```
VITE_API_URL=http://localhost:5001
```

For production deployment on Vercel, the frontend will automatically use relative URLs which will be rewritten to your backend.

If you want to use a custom backend URL in production, update [frontend/src/services/api.js](file:///c%3A/Users/91704/Downloads/SmartServiceToken-2/frontend/src/services/api.js):
```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'
```

## Step 4: Deploy Frontend to Vercel

1. Go to [Vercel Dashboard](https://vercel.com)

2. Click "New Project"

3. Connect your GitHub account and select your repository

4. Configure the project with these settings:
   - Project Name: `smart-service-token-frontend`
   - Framework Preset: Vite
   - Root Directory: `frontend`
   - Build and Output Settings:
     - Build Command: `npm run build`
     - Output Directory: `dist`

5. Add environment variables (only if needed for local development):
   - `VITE_API_URL`: `https://smart-service-token-backend.onrender.com` (your actual Render backend URL)

6. Click "Deploy"

7. Wait for deployment to complete (this may take 2-5 minutes)

8. Once deployed, Vercel will provide you with a URL like:
   `https://smart-service-token-frontend.vercel.app`

## Step 5: Final Configuration

1. Test your application by visiting the frontend URL

2. Log in to the admin panel at `/admin/login` using your credentials

3. Test the API endpoints by submitting a form and checking if emails are sent

## Step 6: Optional Custom Domains

### For Frontend (Vercel):
1. In your Vercel project dashboard, go to "Settings" → "Domains"
2. Add your domain (e.g., `myapp.com`)
3. Follow the DNS configuration instructions provided

### For Backend (Render):
1. In your Render service dashboard, go to "Settings" → "Custom Domains"
2. Add your domain (e.g., `api.myapp.com`)
3. Follow the DNS configuration instructions provided

## Step 7: Redeploy Both Services

After making these changes, redeploy both your frontend on Vercel and backend on Render to ensure all fixes are applied.

## Troubleshooting Common Issues

### 404 Errors on Client-Side Routes
If you encounter 404 errors when accessing routes like `/admin/login` on Vercel:
1. Ensure your [frontend/vercel.json](file:///c%3A/Users/91704/Downloads/SmartServiceToken-2/frontend/vercel.json) has the correct rewrite rules:
   ```json
   {
     "rewrites": [
       {
         "source": "/api/(.*)",
         "destination": "/api"
       },
       {
         "source": "/(.*)",
         "destination": "/index.html"
       }
     ]
   }
   ```
2. Redeploy your frontend on Vercel

### ModuleNotFoundError when deploying to Render
If you encounter a `ModuleNotFoundError: No module named 'app'` error when deploying to Render:
1. Ensure your [backend/app.py](file:///c%3A/Users/91704/Downloads/SmartServiceToken-2/backend/app.py) has an [app](file://c:\Users\91704/Downloads/SmartServiceToken-2/backend/app.py#L0-L62) variable at the module level:
   ```python
   app = create_app()
   ```
2. Ensure your [render.yaml](file:///c%3A/Users/91704/Downloads/SmartServiceToken-2/render.yaml) has the correct start command:
   ```yaml
   startCommand: gunicorn --bind 0.0.0.0:$PORT backend.app:app
   ```
3. Redeploy your backend on Render

### CORS Errors
If you encounter CORS errors:
1. Ensure your backend has CORS enabled in [backend/app.py](file:///c%3A/Users/91704/Downloads/SmartServiceToken-2/backend/app.py):
   ```python
   CORS(app, resources={r"/api/*": {"origins": "*"}})
   ```
2. Redeploy your backend on Render

### Environment Variables Not Loading
1. Double-check that all environment variables are correctly set in both Render and Vercel dashboards
2. Redeploy the affected service

### Database Issues
The application uses SQLite, which is stored on Render's filesystem. For production, consider upgrading to PostgreSQL.

### Slow Initial Load on Render
Render's free tier may put your service to sleep after periods of inactivity. The first request may be slow while the service wakes up.

## Monitoring and Maintenance

### Render (Backend)
1. Monitor logs in the Render dashboard
2. Set up alerts for error monitoring
3. Check the health endpoint: `https://your-backend-url.onrender.com/api/health`

### Vercel (Frontend)
1. Monitor analytics in the Vercel dashboard
2. Check build logs for any issues

## Scaling Considerations

For production use, consider:
1. Upgrading from SQLite to PostgreSQL
2. Adding a CDN for static assets
3. Implementing caching mechanisms
4. Setting up monitoring and alerting
5. Configuring auto-scaling options