# AI Daily Pulse

**Your Daily AI Intelligence Brief** — Curated from 10+ sources, summarized by AI, delivered to your inbox every morning.

## What It Does

AI Daily Pulse aggregates AI news from multiple platforms, uses GPT-4o to generate professional intelligence briefs, and emails them to subscribers daily at 7:00 AM SAST with a detailed PDF attachment.

### Sources
- **Reddit** — r/artificial, r/MachineLearning, r/ChatGPT, r/OpenAI, r/StableDiffusion, r/LocalLLaMA, r/singularity
- **Hacker News** — Top AI-related stories
- **TechCrunch** — AI category
- **The Verge** — AI & Artificial Intelligence
- **Ars Technica** — Technology Lab
- **MIT Technology Review**
- **VentureBeat** — AI category
- **Wired** — AI coverage
- **ArXiv** — cs.AI, cs.LG, cs.CL research papers
- **Product Hunt** — AI tools

### Features
- Multi-platform news aggregation with smart deduplication
- AI-powered summarization (short email + detailed PDF report)
- Daily scheduled delivery at 7 AM SAST
- Web dashboard with full brief history
- Public subscription page
- Manual brief generation trigger
- Source filtering and article archive

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.11+, FastAPI |
| Frontend | React 19, Vite, Tailwind CSS 4 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| AI | OpenAI GPT-4o-mini |
| Email | Resend |
| PDF | FPDF2 |
| Scheduler | APScheduler |
| Hosting | Azure Web Apps |

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- API keys for: OpenAI, Resend, Reddit (optional)

### 1. Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory (copy from `.env.example`):

```env
OPENAI_API_KEY=sk-your-openai-api-key
RESEND_API_KEY=re_your-resend-api-key
REDDIT_CLIENT_ID=your-reddit-client-id
REDDIT_CLIENT_SECRET=your-reddit-client-secret
DATABASE_URL=sqlite:///./ai_daily_pulse.db
FROM_EMAIL=AI Daily Pulse <briefs@aidailypulse.com>
ADMIN_EMAIL=inayethg777@gmail.com
ENVIRONMENT=development
```

Start the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173` and proxies API calls to the backend.

### 3. Get Your API Keys

#### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Add to `.env` as `OPENAI_API_KEY`

#### Resend (Email)
1. Go to https://resend.com
2. Sign up and create an API key
3. Verify your sending domain or use the sandbox
4. Add to `.env` as `RESEND_API_KEY`

#### Reddit (Optional — improves Reddit data quality)
1. Go to https://www.reddit.com/prefs/apps
2. Create a "script" type application
3. Add client ID and secret to `.env`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/stats` | Dashboard statistics |
| POST | `/api/subscribers/` | Subscribe an email |
| DELETE | `/api/subscribers/{email}` | Unsubscribe |
| GET | `/api/subscribers/` | List subscribers |
| GET | `/api/briefs/` | List all briefs |
| GET | `/api/briefs/latest` | Get latest brief |
| GET | `/api/briefs/{id}` | Get brief by ID |
| GET | `/api/briefs/{id}/pdf` | Download brief PDF |
| GET | `/api/articles` | List articles (filter by source/category) |
| POST | `/api/trigger-brief` | Manually trigger brief generation |

---

## Azure Deployment

### Backend (Azure Web App — Python)

1. Create an Azure Web App (Python 3.11)
2. Set the startup command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
3. Add all environment variables from `.env` to Application Settings
4. Deploy via Azure CLI or GitHub Actions

### Frontend (Azure Static Web App or same Web App)

```bash
cd frontend
npm run build
```

The `dist/` folder can be served by the backend or deployed as a separate Azure Static Web App.

---

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Settings & env vars
│   │   ├── database.py          # SQLAlchemy setup
│   │   ├── models.py            # DB models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── routes/
│   │   │   ├── briefs.py        # Brief endpoints
│   │   │   ├── subscribers.py   # Subscriber endpoints
│   │   │   └── news.py          # News & stats endpoints
│   │   └── services/
│   │       ├── news_aggregator.py  # Multi-source news fetching
│   │       ├── summarizer.py       # OpenAI summarization
│   │       ├── pdf_generator.py    # PDF report generation
│   │       ├── email_service.py    # Resend email sending
│   │       └── scheduler.py        # APScheduler daily job
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Landing.jsx      # Landing & subscribe page
│   │   │   ├── Dashboard.jsx    # News dashboard & history
│   │   │   └── BriefDetail.jsx  # Individual brief view
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── SubscribeForm.jsx
│   │   │   └── NewsCard.jsx
│   │   └── api/client.js        # API client
│   ├── package.json
│   └── vite.config.js
└── README.md
```
