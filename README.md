# Lead Management System

## What This Does
Takes incoming leads → AI classifies them as Hot/Warm/Cold → shows everything in a dashboard.

## Architecture
n8n Workflow
    ↓
Python Backend (FastAPI + Groq AI)
    ↓
SQLite Database (leads.db)
    ↓
Next.js Dashboard (localhost:3000)

## How to Run (3 terminals needed)

### Terminal 1 — Backend
cd backend
pip install fastapi uvicorn groq pydantic requests
uvicorn main:app --reload --port 8000

### Terminal 2 — Load sample leads (run once)
cd backend
python seed_leads.py

### Terminal 3 — Frontend
cd frontend
npm install
npm run dev
Then open: http://localhost:3000

### Terminal 4 — n8n automation
n8n start
Then open: http://localhost:5678
Import n8n_workflow.json

## API Endpoints
POST   /lead              → saves lead + classifies with AI
GET    /leads             → returns all leads
POST   /classify          → classify a message only
PATCH  /leads/{id}/status → mark as contacted

## Tools Used
- FastAPI    → Python backend
- Groq AI    → free AI (llama-3.1-8b) for Hot/Warm/Cold classification
- SQLite     → simple local database
- Next.js    → frontend dashboard
- n8n        → automation workflow
- Gmail      → email notification for hot leads

## What I'd Improve With More Time
- Add form in dashboard to submit leads manually
- Deploy to cloud (Railway/Render)
- Add pagination for large datasets
- Use .env file for API keys instead of hardcoding

## Tradeoffs
- SQLite instead of PostgreSQL → simpler, good enough for local use
- Groq instead of Claude API  → free tier, no paid key needed
- Inline CSS instead of Tailwind → one less thing to install