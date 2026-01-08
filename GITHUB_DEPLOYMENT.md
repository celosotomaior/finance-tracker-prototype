# 🚀 GitHub Deployment Checklist

Complete guide to push your Finance Tracker to GitHub and prepare for deployment.

---

## ✅ Step 1: Pre-Flight Checks

### 1.1 Verify Folder Structure

```bash
# From project root
ls -la
```

**Expected structure:**
```
finance-tracker/
├── backend/
│   ├── app/
│   └── requirements.txt
├── frontend/
│   ├── ui/
│   └── requirements.txt
├── .gitignore
├── README.md
└── [other docs]
```

✅ **Status:** Your structure looks good!

### 1.2 Review .gitignore

Your `.gitignore` already covers:
- ✅ Python cache files (`__pycache__/`, `*.pyc`)
- ✅ Virtual environments (`venv/`, `env/`)
- ✅ Environment files (`.env`, `.env.local`)
- ✅ Database files (`*.db`, `*.sqlite`)
- ✅ OS junk (`.DS_Store`, `Thumbs.db`)
- ✅ IDE files (`.vscode/`, `.idea/`)
- ✅ Streamlit cache (`.streamlit/`)

**No changes needed!** 🎉

### 1.3 Create .env.example Template

```bash
# Create backend/.env.example
cat > backend/.env.example << 'EOF'
# Database Configuration
DATABASE_URL=sqlite:///./finance_tracker.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# CORS Settings (comma-separated origins)
ALLOWED_ORIGINS=http://localhost:8501,http://localhost:3000
EOF
```

```bash
# Create frontend/.env.example (if needed)
cat > frontend/.env.example << 'EOF'
# Backend API URL
API_URL=http://localhost:8000/api

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
EOF
```

### 1.4 Verify Secrets Are Ignored

```bash
# Check that .env is properly ignored
cat .gitignore | grep "\.env"
```

Expected output: `.env` and `.env.local` ✅

### 1.5 Remove Sensitive Files (if any)

```bash
# Remove any existing .env files from tracking
find . -name ".env" -type f

# If found, they will automatically be ignored by .gitignore
```

---

## ✅ Step 2: Create GitHub Repository

### **Option A: Using GitHub Website (Manual)**

1. Go to [https://github.com/new](https://github.com/new)
2. Fill in the details:
   - **Repository name:** `finance-tracker-prototype`
   - **Description:** "Personal finance tracker built with FastAPI + Streamlit"
   - **Visibility:** Public or Private (your choice)
   - **⚠️ DO NOT initialize with README, .gitignore, or license** (you already have them)
3. Click **"Create repository"**
4. **Leave the page open** - you'll need the repository URL

### **Option B: Using GitHub CLI (Recommended)**

First, check if you have GitHub CLI installed:

```bash
# Check if gh is installed
gh --version
```

**If not installed:**
```bash
# macOS with Homebrew
brew install gh

# After installation, authenticate
gh auth login
```

**Create the repository:**

```bash
# From your project root
gh repo create finance-tracker-prototype \
  --public \
  --source=. \
  --description "Personal finance tracker built with FastAPI + Streamlit" \
  --push=false
```

> **Note:** If you don't have `gh` installed and don't want to install it, use **Option A** above.

---

## ✅ Step 3: Initialize Git and Push to GitHub

### 3.1 Initialize Git (if not already done)

```bash
# Check if git is already initialized
git status
```

**If you see "not a git repository":**

```bash
# Initialize git
git init

# Set default branch to main
git branch -M main
```

**If git is already initialized:**

```bash
# Just ensure you're on main branch
git branch -M main
```

### 3.2 Stage All Files

```bash
# Add all files (except those in .gitignore)
git add .

# Review what will be committed
git status
```

**❗ CRITICAL CHECK:** Ensure no secrets are staged:

```bash
# Verify .env files are NOT listed
git status | grep -i "\.env$"
# Should return nothing

# Verify .db files are NOT listed
git status | grep "\.db$"
# Should return nothing

# Verify venv/ is NOT listed
git status | grep "venv"
# Should return nothing
```

### 3.3 Create Initial Commit

```bash
# Create your first commit
git commit -m "Initial commit: FastAPI + Streamlit finance tracker

- Backend with FastAPI, SQLAlchemy, Pydantic
- Frontend with Streamlit and Plotly charts
- CRUD operations for income/expense tracking
- Category analysis and balance calculations
- Clean project structure with separation of concerns"
```

### 3.4 Add Remote Repository

**If you used Option A (manual creation):**

```bash
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/finance-tracker-prototype.git

# Verify remote was added
git remote -v
```

**If you used Option B (gh cli):**

The remote should already be set. Verify:

```bash
git remote -v
```

### 3.5 Push to GitHub

```bash
# Push to main branch
git push -u origin main
```

**If prompted for credentials:**
- **Username:** Your GitHub username
- **Password:** Use a **Personal Access Token** (not your GitHub password)
  - Create one at: [https://github.com/settings/tokens](https://github.com/settings/tokens)
  - Scopes needed: `repo` (full control of private repositories)

**Alternative:** Use SSH instead of HTTPS:

```bash
# Remove HTTPS remote
git remote remove origin

# Add SSH remote (replace YOUR_USERNAME)
git remote add origin git@github.com:YOUR_USERNAME/finance-tracker-prototype.git

# Push
git push -u origin main
```

---

## ✅ Step 4: Handle Environment Variables Safely

### 4.1 Confirm .env.example Files Exist

```bash
# Check both were created
ls -la backend/.env.example
ls -la frontend/.env.example  # if you created it
```

### 4.2 Document Environment Variables in README

Add this section to your `README.md` (or create a separate `DEPLOYMENT.md`):

```markdown
## 🔐 Environment Variables

### Backend (.env)

Copy `backend/.env.example` to `backend/.env` and configure:

- `DATABASE_URL`: Database connection string
- `API_HOST`: API server host (default: 0.0.0.0)
- `API_PORT`: API server port (default: 8000)
- `ALLOWED_ORIGINS`: CORS allowed origins

### Frontend (.env)

Copy `frontend/.env.example` to `frontend/.env` and configure:

- `API_URL`: Backend API endpoint

### Deployment Secrets

When deploying to production:

- **Render/Railway (Backend):** Set environment variables in dashboard
- **Streamlit Cloud (Frontend):** Use Secrets management in settings
- **Never commit** `.env` files to version control
```

### 4.3 Store Secrets for Later Deployment

**For Render/Railway (Backend):**
- Dashboard → Environment Variables → Add each variable from `.env.example`

**For Streamlit Cloud (Frontend):**
- App Settings → Secrets → Add in TOML format:
  ```toml
  API_URL = "https://your-backend-url.onrender.com/api"
  ```

**For local development:**
```bash
# Each developer should create their own .env from the example
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

---

## ✅ Step 5: Verification After Push

### 5.1 Check Repository Page

```bash
# Open your repository in browser
open https://github.com/YOUR_USERNAME/finance-tracker-prototype
# Or use: gh repo view --web
```

**Verify:**
- ✅ All files are present (`backend/`, `frontend/`, `README.md`)
- ✅ README displays correctly with formatting
- ✅ `.gitignore` is present
- ✅ Commit message is clear

### 5.2 Verify No Secrets Were Committed

```bash
# Search for .env files in git history
git log --all --full-history -- "*.env"
# Should show NO results (except .env.example)

# Search for database files
git log --all --full-history -- "*.db"
# Should show NO results

# Check current tracked files
git ls-files | grep -E "\.(env|db)$"
# Should only show .env.example files
```

### 5.3 Clone Test (Optional but Recommended)

```bash
# In a temporary location
cd /tmp
git clone https://github.com/YOUR_USERNAME/finance-tracker-prototype.git test-clone
cd test-clone

# Verify structure
ls -la

# Verify .env is NOT present (only .env.example)
ls -la backend/.env
# Should show: No such file or directory ✅

# Clean up
cd ..
rm -rf test-clone
```

---

## ⚠️ Step 6: Emergency - Removing Accidentally Committed Secrets

**If you accidentally committed a `.env` file or secrets:**

### 6.1 Remove from Latest Commit (if not pushed yet)

```bash
# Remove the file
git rm --cached backend/.env

# Amend the commit
git commit --amend --no-edit

# Force push (if already pushed)
git push -f origin main
```

### 6.2 Remove from Git History (for older commits)

```bash
# Install BFG Repo Cleaner (easier than git filter-branch)
brew install bfg

# Remove all .env files from history
bfg --delete-files .env

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push to update remote
git push -f origin main
```

### 6.3 Rotate Compromised Secrets

**⚠️ IMPORTANT:** If secrets were pushed to public repo:
1. **Immediately rotate** all API keys, tokens, passwords
2. Change database passwords
3. Revoke and create new OAuth credentials
4. Check GitHub Security Alerts

### 6.4 Alternative: Nuclear Option (Fresh Start)

If secrets were in many commits:

```bash
# Delete remote repository on GitHub
# Create a new repository
# Create fresh initial commit:

# Remove .git folder
rm -rf .git

# Reinitialize
git init
git branch -M main

# Clean commit
git add .
git commit -m "Initial commit (cleaned)"

# Push to new repository
git remote add origin https://github.com/YOUR_USERNAME/finance-tracker-prototype.git
git push -u origin main
```

---

## 📋 Quick Reference: Common Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# Create a new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Pull latest changes
git pull origin main

# Stage specific files
git add backend/app/main.py

# Commit with message
git commit -m "Add new feature"

# Push to remote
git push origin main

# View remote URLs
git remote -v

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard local changes
git checkout -- filename.py
```

---

## ✅ Next Steps: Deployment

After successfully pushing to GitHub, you can deploy:

1. **Backend (FastAPI):**
   - Render.com (recommended for beginners)
   - Railway.app
   - Fly.io
   - Heroku (paid)

2. **Frontend (Streamlit):**
   - Streamlit Community Cloud (free, easiest)
   - Render.com
   - Railway.app

3. **Database:**
   - Migrate from SQLite to PostgreSQL for production
   - Use managed PostgreSQL (Render, Railway, Supabase)

---

## 📝 Checklist Summary

- [ ] Project structure verified
- [ ] `.gitignore` is comprehensive
- [ ] `.env.example` files created
- [ ] `.env` files are ignored
- [ ] GitHub repository created
- [ ] Git initialized and on `main` branch
- [ ] All files staged (excluding ignored ones)
- [ ] Initial commit created
- [ ] Remote repository added
- [ ] Pushed to GitHub successfully
- [ ] Repository page verified
- [ ] No secrets in git history
- [ ] Documentation updated with deployment notes
- [ ] Ready for deployment! 🚀

---

**🎉 Congratulations!** Your finance tracker is now on GitHub and ready for deployment.

**Questions or Issues?**
- Check GitHub's [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- Review [GitHub CLI docs](https://cli.github.com/manual/)
- See deployment guides for [Render](https://render.com/docs) and [Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
