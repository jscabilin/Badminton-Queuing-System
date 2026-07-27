# 🏸 Badminton Queue & Fair-Play System

A web app for running fair, well-managed badminton sessions — auto-assigns players to courts based on play count, tracks skill tiers (Beginner → Advance), and suggests level-ups based on match results.

Built as a personal learning project: HTML/CSS/JS frontend, FastAPI backend, Supabase (Postgres) database.

📄 Full planning docs are in [`/docs`](./docs): [PRD](./docs/PRD.md) · [Architecture](./docs/ARCHITECTURE.md) · [Design](./docs/DESIGN.md) · [Rules](./docs/RULES.md) · [Plan](./docs/PLAN.md)

---

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | HTML, CSS, vanilla JavaScript |
| Backend | Python 3.11+, FastAPI |
| Database | Supabase (Postgres) |
| Frontend Hosting | Vercel |
| Backend Hosting | Render (or Railway) |

---

## Project Structure

```
Badminton-Queuing-System/
├── frontend/           # HTML/CSS/JS
│   ├── index.html
│   ├── style.css
│   └── app.js
├── backend/            # FastAPI
│   ├── main.py
│   ├── requirements.txt
│   └── .env            # NOT committed — see below
├── docs/               # planning docs (PRD, Architecture, Design, Rules, Plan)
├── .gitignore
├── LICENSE
└── README.md
```

---

## Prerequisites

Install these before you start:

- **Python 3.11+** — [python.org/downloads](https://www.python.org/downloads/)
- **Git** — [git-scm.com](https://git-scm.com/)
- A code editor (VS Code recommended)
- A free [Supabase](https://supabase.com) account
- A free [Vercel](https://vercel.com) account (for later, when deploying the frontend)

---

## 1. Clone the Repo

```bash
git clone https://github.com/jscabilin/Badminton-Queuing-System.git
cd Badminton-Queuing-System
```

## 2. Set Up Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **Project Settings → API** and copy:
   - Project URL
   - `anon` public key
3. Go to the **SQL Editor** in Supabase and create your tables (see schema in [`docs/DESIGN.md`](./docs/DESIGN.md))

## 3. Backend Setup (FastAPI)

```bash
cd backend

# create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# install dependencies
pip install fastapi uvicorn supabase python-dotenv
pip freeze > requirements.txt
```

Create a `backend/.env` file (this is gitignored — never commit it):

```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

**Run the backend locally:**

```bash
uvicorn main:app --reload
```

- API runs at: `http://127.0.0.1:8000`
- Auto-generated API docs: `http://127.0.0.1:8000/docs` (FastAPI gives you this for free — great for testing endpoints as you build them)

## 4. Frontend Setup

No build step needed — it's plain HTML/CSS/JS. Just open it with a local server so `fetch()` calls work properly (opening the HTML file directly via `file://` can cause CORS issues).

**Easiest option — Python's built-in server:**

```bash
cd frontend
python -m http.server 5500
```

Then open `http://127.0.0.1:5500` in your browser.

**Or, if you use VS Code:** install the "Live Server" extension and click "Go Live" at the bottom right.

Make sure your `app.js` points to your local backend URL, e.g.:

```js
const API_URL = "http://127.0.0.1:8000";
```

---

## Running Both Together (Local Dev)

You'll need two terminals open:

```bash
# Terminal 1 — backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 2 — frontend
cd frontend
python -m http.server 5500
```

---

## Deployment

### Deploy the Frontend to Vercel

1. Push your code to GitHub (already done ✅)
2. Go to [vercel.com](https://vercel.com) → **Add New Project**
3. Import your `Badminton-Queuing-System` repo
4. Set the **Root Directory** to `frontend`
5. Framework preset: **Other** (since it's plain HTML/CSS/JS, no build command needed)
6. Click **Deploy**
7. Update `API_URL` in `app.js` to point to your deployed backend URL (see below) before deploying, or use an environment variable if you set one up

### Deploy the Backend to Render

1. Go to [render.com](https://render.com) → **New Web Service**
2. Connect your GitHub repo, set **Root Directory** to `backend`
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables `SUPABASE_URL` and `SUPABASE_KEY` in Render's dashboard (same values as your local `.env`)
6. Deploy — Render will give you a live URL like `https://your-app.onrender.com`
7. Update your frontend's `API_URL` to this URL and redeploy on Vercel

> **Note:** Render's free tier spins down after inactivity, so your first request after idle time may take ~30 seconds to wake up. Fine for a learning project, worth knowing so it doesn't confuse you later.

---

## Where to Go From Here

Check [`docs/PLAN.md`](./docs/PLAN.md) for the phased build order — start at Phase 0 and work through it. Don't jump to the promotion/level-up logic until the basic queue is working end-to-end.

---

## License

MIT — see [LICENSE](./LICENSE)
