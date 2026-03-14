# Deployment Guide

## Option 1: Coolify (Free - Recommended)

### Steps:
1. Go to https://coolify.io
2. Sign up / Install self-hosted
3. Create new project
4. Add GitHub repository: https://github.com/yusufdupsc1/sso-platform
5. Set environment variables
6. Deploy

### Environment Variables:
```
POSTGRES_DB=sso_platform
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
DJANGO_SECRET=your_secret_key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
```

---

## Option 2: Railway

### Steps:
1. Go to https://railway.app
2. Sign up with GitHub
3. New Project → Deploy from GitHub repo
4. Add environment variables
5. Deploy

---

## Option 3: Render

### Steps:
1. Go to https://render.com
2. Sign up with GitHub
3. New Web Service
4. Connect GitHub repo
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `gunicorn sso_platform.wsgi:application`
7. Deploy

---

## Frontend (Next.js)

Deploy frontend to Vercel:
1. Go to https://vercel.com
2. Import GitHub repo
3. Deploy
