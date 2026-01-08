# 🚀 Streamlit Cloud Deployment Guide

Complete step-by-step guide to deploy your Finance Tracker to production.

---

## 📋 Prerequisites

### What You'll Need

- [x] GitHub repository with your code pushed
- [ ] [Render.com](https://render.com) account (free)
- [ ] [Streamlit Community Cloud](https://streamlit.io/cloud) account (free)
- [ ] Your repository must be **public** (Streamlit Cloud free tier requirement)

---

## 🎯 Deployment Architecture

```
┌─────────────────┐         ┌──────────────────┐
│  Streamlit      │  HTTP   │   FastAPI        │
│  Cloud          │ ───────>│   Backend        │
│  (Frontend)     │ Requests│   (Render.com)   │
└─────────────────┘         └──────────────────┘
                                    │
                                    ▼
                              ┌──────────┐
                              │  SQLite  │
                              │  Database│
                              └──────────┘
```

---

## Part 1: Deploy Backend (FastAPI to Render)

### Step 1.1: Create Render Configuration

Create `backend/render.yaml`:

```yaml
services:
  - type: web
    name: finance-tracker-backend
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: PORT
        sync: false
```

**Create this file:**

```bash
cat > backend/render.yaml << 'EOF'
services:
  - type: web
    name: finance-tracker-backend
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
EOF
```

### Step 1.2: Update CORS for Production

Your backend needs to accept requests from Streamlit Cloud. We'll check your current CORS settings and update if needed.

**You'll need to add the Streamlit Cloud domain to allowed origins.**

### Step 1.3: Commit and Push

```bash
# Add new files
git add backend/render.yaml
git add frontend/.streamlit/config.toml

# Commit
git commit -m "Add deployment configuration for Render and Streamlit Cloud"

# Push
git push origin main
```

### Step 1.4: Deploy on Render

1. **Go to Render:** [https://dashboard.render.com](https://dashboard.render.com)
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub repository:** `finance-tracker-prototype`
4. **Configure:**
   - **Name:** `finance-tracker-backend`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`

5. **Environment Variables:**
   - Add: `PYTHON_VERSION` = `3.11.0`
   - Add: `DATABASE_URL` = `sqlite:///./finance_tracker.db`

6. **Click "Create Web Service"**

### Step 1.5: Wait for Deployment

- Render will build and deploy your backend (~2-5 minutes)
- Watch the logs for any errors
- When it shows **"Live"**, copy the URL

**Your backend URL will be:**
```
https://finance-tracker-backend-XXXX.onrender.com
```

### Step 1.6: Test Backend

```bash
# Replace with your actual Render URL
curl https://YOUR-BACKEND-URL.onrender.com/api/items

# Should return: []
```

**Or open in browser:**
```
https://YOUR-BACKEND-URL.onrender.com/docs
```

✅ If you see the Swagger docs, backend is working!

---

## Part 2: Deploy Frontend (Streamlit to Cloud)

### Step 2.1: Update Frontend API Configuration

Before deploying, frontend needs to use the production backend URL.

**Check your frontend code** - we'll update it to read from Streamlit secrets.

### Step 2.2: Create Streamlit Account

1. Go to [https://share.streamlit.io/](https://share.streamlit.io/)
2. **Sign up** with GitHub
3. **Authorize** Streamlit to access your repositories

### Step 2.3: Deploy App

1. **Click "New app"**
2. **Configure:**
   - **Repository:** `YOUR-USERNAME/finance-tracker-prototype`
   - **Branch:** `main`
   - **Main file path:** `frontend/ui/app.py`
   - **App URL:** `finance-tracker` (or your preferred subdomain)

3. **Click "Advanced settings"** (before deploying)

### Step 2.4: Configure Secrets

In the **Secrets** section, add:

```toml
# Backend API URL (replace with your Render URL)
API_URL = "https://YOUR-BACKEND-URL.onrender.com/api"
```

**Example:**
```toml
API_URL = "https://finance-tracker-backend-abc123.onrender.com/api"
```

4. **Click "Deploy!"**

### Step 2.5: Wait for Deployment

- Streamlit will install dependencies (~1-2 minutes)
- Watch the deployment logs
- App will automatically open when ready

**Your app URL will be:**
```
https://YOUR-APP.streamlit.app
```

---

## Part 3: Update Backend CORS

Now that you have your Streamlit URL, update backend to allow it:

### Step 3.1: Update CORS Origins

**Edit `backend/app/main.py`** and update CORS middleware:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Local development
        "https://YOUR-APP.streamlit.app",  # ← Add your Streamlit URL
        "https://*.streamlit.app",  # Allow all Streamlit Cloud apps
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Step 3.2: Push Update

```bash
git add backend/app/main.py
git commit -m "Update CORS to allow Streamlit Cloud domain"
git push origin main
```

Render will **automatically redeploy** your backend (~2 min).

---

## ✅ Verification Checklist

### Backend (Render)

- [ ] Deployment status shows "Live"
- [ ] `/docs` endpoint loads Swagger UI
- [ ] `GET /api/items` returns valid JSON
- [ ] `POST /api/items` can create new items
- [ ] No errors in Render logs

**Test command:**
```bash
curl -X POST https://YOUR-BACKEND-URL.onrender.com/api/items \
  -H "Content-Type: application/json" \
  -d '{
    "type": "income",
    "category": "Test",
    "amount": 100.00,
    "date": "2026-01-07",
    "description": "Deployment test"
  }'
```

### Frontend (Streamlit Cloud)

- [ ] App loads without errors
- [ ] Can create new income/expense items
- [ ] Items appear in the table
- [ ] Charts render correctly
- [ ] Filters work (category, date)
- [ ] Can delete items
- [ ] Balance calculation is correct

### End-to-End Test

1. **Create an income:** $5000 - Salary
2. **Create an expense:** $200 - Groceries
3. **Verify balance:** Shows $4800
4. **Check chart:** Both categories appear
5. **Filter by category:** Works correctly
6. **Delete an item:** Removes successfully

---

## 🔧 Troubleshooting

### Backend Issues

**Problem:** "This service is unavailable"
- **Solution:** Render free tier sleeps after 15 min. First request takes ~30s to wake up.

**Problem:** CORS errors in browser console
- **Solution:** Add your Streamlit domain to CORS allowed origins (see Part 3)

**Problem:** Database resets on restart
- **Solution:** Expected with SQLite on free tier. Upgrade to PostgreSQL for persistence.

### Frontend Issues

**Problem:** "Connection refused" or API errors
- **Solution:**
  1. Check Streamlit secrets have correct backend URL
  2. Ensure backend is awake (visit `/docs` first)
  3. Check browser console for CORS errors

**Problem:** "ModuleNotFoundError"
- **Solution:** Verify `requirements.txt` includes all dependencies

**Problem:** App crashes or shows "😟 Oh no"
- **Solution:**
  1. Check Streamlit logs in dashboard
  2. Look for Python errors in stack trace
  3. Test API URL manually with curl

---

## 📊 Monitor Your Apps

### Render Dashboard

- **Logs:** See real-time backend logs
- **Metrics:** Request count, response times
- **Events:** Deployment history

### Streamlit Dashboard

- **Logs:** View frontend errors
- **Analytics:** User activity (if enabled)
- **Secrets:** Update API URL anytime

---

## 🚀 Post-Deployment

### Share Your App!

Your app is now live:

- **Frontend:** `https://YOUR-APP.streamlit.app`
- **Backend API:** `https://YOUR-BACKEND.onrender.com/docs`

### Update README

Add to your `README.md`:

```markdown
## 🌐 Live Demo

- **App:** https://YOUR-APP.streamlit.app
- **API Docs:** https://YOUR-BACKEND.onrender.com/docs

> Note: Free tier apps may take ~30s to wake up from sleep.
```

### Known Limitations (Free Tier)

- **Data Persistence:** SQLite data resets on Render restart
- **Cold Starts:** 15-30 second delay after inactivity
- **Concurrency:** Limited concurrent users
- **Uptime:** May sleep during low usage

### Upgrade Path

**For production use:**
1. **Database:** Migrate to Render PostgreSQL ($7/mo)
2. **Backend:** Upgrade Render instance for faster startup
3. **Monitoring:** Add Sentry for error tracking
4. **CI/CD:** Set up GitHub Actions for automated tests

---

## 🎉 You're Live!

Congratulations! Your Finance Tracker is now deployed and accessible worldwide.

**Next steps:**
- Test all features
- Share with friends
- Monitor usage
- Consider upgrades for production

**Questions?** Check:
- [Render Docs](https://render.com/docs)
- [Streamlit Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
