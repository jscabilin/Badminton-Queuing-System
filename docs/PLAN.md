# Project Plan
## Badminton Queue & Fair-Play System

No hard deadline — this is a learn-as-you-go project. Phases are ordered so each one gives you a working, demoable thing before you add complexity. Check items off as you go.

### Phase 0 — Setup
- [ ] Create GitHub repo, add these 5 docs to a `/docs` folder
- [ ] Create a Supabase project, note down your project URL and anon key
- [ ] Set up local folders: `/frontend` (HTML/CSS/JS) and `/backend` (FastAPI)
- [ ] Get a bare FastAPI app running locally (`GET /health` returning `{"status": "ok"}`)
- [ ] Connect FastAPI to Supabase (test with a simple query)

### Phase 1 — MVP Core: Players, Sessions, Manual Queue
- [ ] Build `players` and `groups` tables in Supabase
- [ ] `POST /players`, `GET /players` endpoints
- [ ] Simple frontend page: add a player, list all players with their tier
- [ ] Build `sessions` and `courts` tables
- [ ] `POST /sessions` to start a session with N courts
- [ ] **Milestone:** you can add players and start a session from the UI

### Phase 2 — Queue Engine + Match Logging
- [ ] Build `matches` and `match_players` tables
- [ ] Implement the Fair Queue Engine (sort by play count, assign next N)
- [ ] `GET /sessions/{id}/queue` and `POST /sessions/{id}/assign` endpoints
- [ ] `POST /matches` endpoint — logs a match, updates `total_games_played`
- [ ] Frontend Queue View + Log Match screen
- [ ] **Milestone:** you can run a real session end-to-end (queue → assign → log → repeat)

### Phase 3 — Skill Tiers + Promotion Suggestions
- [ ] Add `current_tier` to players, `tier_history` table
- [ ] Build `promotion_suggestions` table
- [ ] Implement `suggest_promotion()` per RULES.md logic, run it after each match log
- [ ] Promotion Review screen (approve/dismiss)
- [ ] **Milestone:** the system flags its first real level-up suggestion

### Phase 4 — Multi-Group Support + Player Self-View
- [ ] Ensure all queries are properly scoped by `group_id` (no data leaking between groups)
- [ ] Add Supabase Auth — players get a login to view only their own stats
- [ ] `GET /players/{id}/stats` + Player Stats View screen
- [ ] **Milestone:** two different groups can use the same deployed app independently

### Phase 5 — Stretch Goals (pick based on what excites you)
- [ ] Replace rule-based promotion logic with a basic ML/statistical model (e.g., logistic regression using match history features)
- [ ] Real-time queue updates (Supabase Realtime or WebSockets) instead of manual refresh
- [ ] Migrate frontend to a framework (React) once vanilla JS starts feeling limiting
- [ ] Mobile-optimized / installable as a PWA for courtside use
- [ ] Demotion logic, score-margin-weighted promotion scoring

### Notes for "Vibe Coding" Sessions
- Keep this PLAN.md updated as your source of truth for "what's next" — when you sit down to vibe code, open this file first and pick the next unchecked item.
- It's fine to jump ahead for fun (e.g., prototype the UI before the backend exists) — just come back and fill in the phase order once the fun exploration is done.
- Commit often, even messy commits — this is a learning repo, not a polished portfolio piece (yet).
