# Deployment Guide

## Streamlit Cloud Deployment (Recommended)

### Step 1: Push to GitHub

1. Initialize git repository (if not already done):
```bash
git init
git add .
git commit -m "Initial commit - Program Impact Dashboard"
```

2. Create a new repository on GitHub (github.com)

3. Push your code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/impact_metrics.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)

2. Sign in with your GitHub account

3. Click "New app"

4. Configure:
   - **Repository**: Select your `impact_metrics` repository
   - **Branch**: `main`
   - **Main file**: `dashboard.py`
   - **App URL**: Choose a unique name (e.g., `impact-dashboard-mvp`)

5. Click "Deploy!"

6. Your app will be live at: `https://YOUR-APP-NAME.streamlit.app`

### Step 3: Update Data Files

After deployment, you can:
- Upload CSV files via the dashboard UI
- Or keep sample data files in the repository
- Or connect to external data sources (Google Sheets, databases, etc.)

## Alternative Deployment Options

### Local Network Access

Run on your local network:
```bash
streamlit run dashboard.py --server.address 0.0.0.0
```

Access from other devices on the same network using: `http://YOUR_IP:8501`

### Docker Deployment

1. Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. Build and run:
```bash
docker build -t impact-dashboard .
docker run -p 8501:8501 impact-dashboard
```

### Manual Deployment Checklist

Before deploying, ensure:
- [x] All dependencies are in `requirements.txt`
- [x] Sample data files are included (or document data upload process)
- [x] No hardcoded paths or local-only resources
- [x] README.md documents usage
- [x] `.gitignore` excludes unnecessary files

## Required Files for Deployment

- `dashboard.py` - Main application
- `requirements.txt` - Python dependencies
- `Expectations.csv` - Sample expectations data
- `Performance.csv` - Sample performance data
- `Evidence.csv` - Sample evidence data
- `metric_rationale.json` - Metric explanations (optional)

## Post-Deployment

1. Test all functionality
2. Share the URL with your team
3. Update data files as needed
4. Monitor usage and gather feedback

