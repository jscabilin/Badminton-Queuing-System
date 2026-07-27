# Architecture Document
## Badminton Queue & Fair-Play System

### 1. Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | HTML, CSS, vanilla JavaScript | You already know this. No framework yet — focus your learning on real app logic (state, API calls, rendering) before adding React/Vue complexity later. |
| Backend | Python + FastAPI | Beginner-friendly, gives you free auto-generated API docs (`/docs`), and is where your rule-based (later ML-based) promotion logic lives. |
| Database | Supabase (Postgres) | You know basic SQL already. Supabase gives you a real Postgres DB, free hosting tier, and built-in auth for the "players view their own stats" feature later. |
| Hosting (frontend) | Vercel or Netlify (free tier) | Simple static hosting, deploys straight from GitHub. |
| Hosting (backend) | Render or Railway (free tier) | Easy FastAPI deployment, minimal config. |
| Auth | Supabase Auth | Since players will eventually log in to view their own stats, don't roll your own auth — use Supabase's. |

### 2. High-Level System Diagram

```
[Browser: HTML/CSS/JS]
        |
        | HTTP (fetch/JSON)
        v
[FastAPI Backend]
   |-- API routes (players, sessions, matches, queue)
   |-- Business logic layer
   |      |-- Queue engine (fair rotation)
   |      |-- Promotion engine (rule-based, pluggable for future ML)
   |-- Supabase client (DB access)
        |
        v
[Supabase (Postgres) Database]
   |-- players, sessions, courts, matches, tier_history tables
```

### 3. Component Breakdown

**Frontend (HTML/CSS/JS)**
- Views: Session Dashboard, Queue View, Player Stats View, Admin (Player/Session Management)
- Talks to the backend only via `fetch()` calls to FastAPI endpoints — never touches Supabase directly. This keeps your backend as the single source of truth and gives you real practice building/consuming an API.

**Backend (FastAPI)**
- `/players` — CRUD for player records and skill tags
- `/sessions` — create/manage a session (courts count, date, group)
- `/queue` — get the current fair queue, assign next players to a court
- `/matches` — log a completed match (updates play counts automatically)
- `/promotions` — list current level-up suggestions for organizer review

**Business Logic Layer (inside FastAPI, kept separate from route handlers)**
- **Queue Engine**: sorts waiting players by play count (ascending), picks the next N for open courts, with tie-breaking (e.g., longest time waiting)
- **Promotion Engine**: a plain Python function today (`suggest_promotion(player) -> bool`) that takes a player's match history and applies the rules in RULES.md. Designed as a single swappable function/interface so a real ML model can replace the internals later without touching the rest of the app.

**Database (Supabase/Postgres)**
- See DESIGN.md for full schema. Core tables: `players`, `groups`, `sessions`, `courts`, `matches`, `tier_history`.

### 4. Data Flow Example: Logging a Match
1. Organizer selects 4 players on a court in the UI and submits the result.
2. Frontend sends `POST /matches` with player IDs, court, winner/score.
3. Backend writes the match row to Supabase, increments each player's play count.
4. Backend runs the Promotion Engine against the affected players.
5. If a promotion is suggested, it's written to a `promotion_suggestions` table (or flagged status) for the organizer to review — not auto-applied.
6. Backend recalculates the queue and returns the updated state to the frontend.

### 5. Why This Structure Supports Your Learning Goals
- You practice **full-stack thinking**: UI → API → business logic → database, not just calling a hosted service directly.
- The **Promotion Engine is isolated** on purpose — it's the one part of the app most likely to change (rules today, ML tomorrow), so it's built as a single-responsibility module from day one.
- Because sessions/groups are modeled as their own entities (not hardcoded), you get real practice with **relational database design** and multi-tenant-style thinking, even at small scale.

### 6. Future Extension Points (don't build yet, just know they exist)
- Swap `suggest_promotion()` internals for a trained model (e.g., logistic regression on match history) — same function signature, no other code changes needed.
- Add real-time updates (WebSockets or Supabase Realtime) once polling feels too slow.
- Add a proper frontend framework once the vanilla JS app starts feeling hard to maintain.
