# Project Plan
## Badminton Queue & Fair-Play System

This plan is written as a learning roadmap. Each phase should end with something working that you can open, test, and explain.

The goal is not to build everything at once. The goal is to build one small full-stack slice at a time: database -> API -> frontend -> test -> repeat.

### How to use this plan

- Work in order.
- Do not start the next phase until the current one is testable.
- If a task feels too big, split it into a smaller version that returns JSON or renders one simple screen.
- Keep the backend as the source of truth. The frontend should only call your API and render the result.
- After each phase, write one short note in the repo about what you learned.

### Phase 0 - Setup and project skeleton

Goal: get the repo running locally and confirm you can talk to Supabase.

What you should create:

- `frontend/index.html`
- `frontend/style.css`
- `frontend/app.js`
- `backend/main.py`
- `backend/requirements.txt`
- `backend/.env` for local use only
- `backend/.env.example` for safe sharing

Steps:

1. Create a Supabase project.
2. Copy the project URL and anon key into `backend/.env`.
3. Create the `frontend` and `backend` folders if they do not exist.
4. Build a tiny FastAPI app with a `GET /health` route that returns `{"status": "ok"}`.
5. Add one test route or startup log that proves the backend is running.
6. Add a simple Supabase connection test from the backend.
7. Run the backend locally and open the FastAPI docs page.
8. Run the frontend with a local static server and make sure the page loads.

What you learn:

- Python virtual environments
- Environment variables
- FastAPI startup and routing
- Basic HTTP requests
- How Supabase credentials are stored and used

Done when:

- `GET /health` works locally
- The backend can connect to Supabase
- The frontend loads in a browser

### Phase 1 - Database basics and player CRUD

Goal: create and read groups and players.

What you should create:

- Supabase tables: `groups`, `players`
- Backend modules for database access and request models
- Endpoints for creating and reading players
- A simple frontend form for adding a player and listing players

Steps:

1. Create the `groups` table.
2. Create the `players` table with a foreign key to `groups`.
3. Decide the minimum fields for each table and write them down before coding.
4. Create backend data models for group and player payloads.
5. Add `POST /groups` so you can create a group.
6. Add `POST /players` so you can add a player to a group.
7. Add `GET /players` so you can list players.
8. Test the routes in FastAPI docs before touching the frontend.
9. Build a very simple frontend form that posts a player.
10. Render the player list from the API in the browser.

What you learn:

- Relational database basics
- CRUD endpoints
- Request validation
- Rendering API data in plain JavaScript

Done when:

- You can create a group
- You can add players to that group
- You can refresh the page and still see the data from the database

### Phase 2 - Sessions and courts

Goal: create a session with courts and display the session state.

What you should create:

- Supabase tables: `sessions`, `courts`
- Backend endpoint for creating a session
- Frontend session creation form
- A session dashboard screen

Steps:

1. Create the `sessions` table.
2. Create the `courts` table with a foreign key to `sessions`.
3. Decide what a session must contain: name, group, date, court count, status.
4. Add `POST /sessions`.
5. When a session is created, automatically create the correct number of court rows.
6. Add `GET /sessions/{id}` or a similar read endpoint.
7. Build a dashboard page that shows the active session and its courts.
8. Test creating sessions with different court counts.

What you learn:

- Parent-child records
- Creating multiple rows from one request
- State management across related tables
- Basic session-based app design

Done when:

- You can create a session from the UI
- The session shows the right number of courts
- You can read the session back from the backend

### Phase 3 - Fair queue engine

Goal: generate a fair queue and assign the next players to courts.

What you should create:

- A pure Python queue function
- `GET /sessions/{id}/queue`
- `POST /sessions/{id}/assign`
- A queue view in the frontend

Steps:

1. Write the queue rule in plain English before coding.
2. Implement sorting by `total_games_played` ascending.
3. Add tie-breakers for longest time since last match and then join order.
4. Make the queue logic a pure function if possible.
5. Add `GET /sessions/{id}/queue`.
6. Add `POST /sessions/{id}/assign`.
7. Have assign move the top players into open courts.
8. Show waiting players and open courts in the frontend.
9. Test with a small fake dataset first.
10. Break the queue on purpose once, then fix it. That is part of the learning.

What you learn:

- Business logic separation
- Deterministic sorting
- Pure functions
- Testing edge cases

Done when:

- You can press one button and assign the next players fairly
- The order matches your rules
- You can explain why a given player was chosen

### Phase 4 - Match logging and play counts

Goal: log match results and update player counts correctly.

What you should create:

- Supabase tables: `matches`, `match_players`
- `POST /matches`
- A log match form in the frontend
- Automatic updates to `total_games_played`

Steps:

1. Create the `matches` table.
2. Create the `match_players` table.
3. Decide whether you want singles, doubles, or both for the first version.
4. Add `POST /matches`.
5. Save who played, who won, the court, and the time.
6. Update player game counts after the match is saved.
7. Store the opponent tier snapshot at match time.
8. Add a frontend form for logging the match result.
9. Re-fetch the queue after logging a match.
10. Verify the data in Supabase after each test.

What you learn:

- Write operations that affect multiple tables
- Keeping counters in sync
- Why snapshots matter in history data
- How to debug state changes after a save

Done when:

- A match can be logged from the UI
- Game counts update correctly
- The queue changes after a match is completed

### Phase 5 - Skill tiers and promotion suggestions

Goal: add the actual fair-play logic around player progression.

What you should create:

- `current_tier` on `players`
- `tier_history`
- `promotion_suggestions`
- `suggest_promotion()` in the backend
- Approve and dismiss actions in the frontend

Steps:

1. Add tier fields to the player model and database.
2. Create the `tier_history` table for auditability.
3. Create the `promotion_suggestions` table.
4. Write the promotion rule from `docs/RULES.md` in code.
5. Keep the rule-based logic in one function.
6. Trigger the suggestion check after each match is logged.
7. Make sure duplicate pending suggestions are not created.
8. Add an admin review screen for pending suggestions.
9. Implement approve and dismiss actions.
10. Record approved changes in `tier_history`.

What you learn:

- Domain rules in code
- Audit trails
- Human review flows
- Keeping logic easy to change later

Done when:

- The backend can suggest a promotion
- The suggestion is visible in the UI
- The organizer can approve or dismiss it

### Phase 6 - Multi-group support and player view

Goal: make the app safe for multiple groups and useful for players too.

What you should create:

- Scoped queries that always filter by `group_id`
- Supabase Auth
- `GET /players/{id}/stats`
- A read-only stats page

Steps:

1. Review every query and make sure it is scoped to one group.
2. Add a player login flow with Supabase Auth.
3. Decide what a player is allowed to see.
4. Build the stats endpoint.
5. Show games played, tier, and recent matches.
6. Add a read-only frontend screen for player stats.
7. Test with at least two groups.
8. Confirm one group cannot see the other group's data.

What you learn:

- Authentication
- Authorization
- Data isolation
- Safer API design

Done when:

- Two groups can use the same app without leaking data
- A player can see their own stats
- The organizer and player views are different on purpose

### Phase 7 - Deployment and polish

Goal: put the project online and make it usable in a real session.

What you should create:

- Deployed backend
- Deployed frontend
- Production environment variables
- A short setup note for future you

Steps:

1. Deploy the backend to Render or Railway.
2. Deploy the frontend to Vercel.
3. Set production environment variables.
4. Test the full flow from the deployed frontend.
5. Check the app on a phone.
6. Fix the rough parts that make live use annoying.
7. Write a short deployment note in the repo.

What you learn:

- Deployment basics
- Production environment configuration
- Real-device testing
- Debugging outside local development

Done when:

- You can use the app from a deployed URL
- The core flow works on mobile
- The project is good enough for a real badminton session

### Suggested build order inside every phase

Use this loop for each feature:

1. Define the data you need.
2. Create or update the database table.
3. Build the backend endpoint.
4. Test the endpoint in FastAPI docs.
5. Wire the frontend to the endpoint.
6. Test the full flow in the browser.
7. Fix the bugs before moving on.

### What to leave for later

Do not start these until the queue, match logging, and tiering all work:

- React or another frontend framework
- Machine learning promotion logic
- Real-time updates
- Demotion logic
- Fancy visual design

### Learning mindset for this project

- Build the smallest version that proves the idea.
- Keep a working app after every phase.
- If you do not understand a piece, stop and isolate it.
- Make the app teach you one new thing at a time.
- Update this file as the project grows so it stays your real roadmap.
