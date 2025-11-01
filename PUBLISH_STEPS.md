# Quick Publish Steps

## Step 1: Initialize Git Repository

Open terminal/PowerShell in this folder and run:

```bash
git init
git add .
git commit -m "Initial commit - Program Impact Dashboard MVP"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `impact-dashboard-mvp`)
3. **DO NOT** initialize with README (we already have files)
4. Copy the repository URL (e.g., `https://github.com/YOUR_USERNAME/impact-dashboard-mvp.git`)

## Step 3: Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/impact-dashboard-mvp.git
git branch -M main
git push -u origin main
```

## Step 4: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `impact-dashboard-mvp`
5. Branch: `main`
6. Main file path: `dashboard.py`
7. App URL: Choose a name (e.g., `impact-dashboard-mvp`)
8. Click "Deploy!"

## Step 5: Access Your Published Dashboard

Your dashboard will be live at:
`https://impact-dashboard-mvp.streamlit.app`

(Replace `impact-dashboard-mvp` with your chosen app name)

---

## Alternative: Manual Git Commands

If you prefer, I can run these commands for you. Just let me know!

