# Design Document
## Badminton Queue & Fair-Play System

### 1. Database Schema (Supabase / Postgres)

**`groups`** — a club/barkada that owns its own players and sessions
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| name | text | e.g. "Weekend Warriors" |
| created_at | timestamp | |

**`players`**
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| group_id | uuid, FK → groups.id | |
| name | text | |
| current_tier | text | enum: beginner, lower_intermediate, higher_intermediate, advance |
| total_games_played | int | denormalized counter, updated on match log |
| created_at | timestamp | |

**`sessions`** — one specific play day/event
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| group_id | uuid, FK → groups.id | |
| name | text | e.g. "July 28 Session" |
| court_count | int | fixed number of courts for this session |
| date | date | |
| status | text | enum: active, completed |

**`courts`**
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| session_id | uuid, FK → sessions.id | |
| court_number | int | |
| status | text | enum: open, in_use |

**`matches`**
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| session_id | uuid, FK → sessions.id | |
| court_id | uuid, FK → courts.id | |
| player_ids | uuid[] or join table `match_players` | supports 2 or 4 players (singles/doubles) |
| winner_ids | uuid[] | nullable if score-based instead of win/loss |
| score | text | optional, e.g. "21-18" |
| played_at | timestamp | |

**`match_players`** (if not using array column — recommended for clean SQL joins)
| Column | Type | Notes |
|---|---|---|
| match_id | uuid, FK → matches.id | |
| player_id | uuid, FK → players.id | |
| is_winner | boolean | |
| opponent_tier | text | snapshot of the *opponent's* tier at match time (important for promotion logic — see RULES.md) |

**`tier_history`** — every tier change, with reason
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| player_id | uuid, FK → players.id | |
| old_tier | text | |
| new_tier | text | |
| reason | text | e.g. "organizer-approved suggestion" |
| changed_at | timestamp | |

**`promotion_suggestions`**
| Column | Type | Notes |
|---|---|---|
| id | uuid, PK | |
| player_id | uuid, FK → players.id | |
| suggested_tier | text | |
| reason_summary | text | human-readable explanation, e.g. "3 wins vs Higher Intermediate in last 10 games" |
| status | text | enum: pending, approved, dismissed |
| created_at | timestamp | |

### 2. API Contract (FastAPI routes)

| Method | Route | Purpose |
|---|---|---|
| POST | `/groups` | Create a group |
| POST | `/players` | Add a player to a group |
| PATCH | `/players/{id}` | Edit player (name, manual tier override) |
| POST | `/sessions` | Start a new session (group_id, court_count, date) |
| GET | `/sessions/{id}/queue` | Get current fair queue + court status |
| POST | `/sessions/{id}/assign` | Auto-assign next players to an open court |
| POST | `/matches` | Log a completed match |
| GET | `/players/{id}/stats` | Player self-view: games played, tier, recent matches |
| GET | `/promotions?status=pending` | List pending level-up suggestions |
| POST | `/promotions/{id}/approve` | Organizer approves a suggested tier change |
| POST | `/promotions/{id}/dismiss` | Organizer dismisses a suggestion |

### 3. UI Screens (v1)

1. **Session Dashboard** — pick/create a session, see court count and status at a glance
2. **Queue View** — live list of who's waiting (ordered by fairness), which courts are open/in-use, a big "Assign Next" button
3. **Log Match** — quick form: pick court, pick winner(s)/score, submit
4. **Player Management (Admin)** — add/edit players, set initial tier, view all players in a group
5. **Promotion Review (Admin)** — list of pending suggestions with the reason, approve/dismiss buttons
6. **Player Stats View** — read-only page a player can open: their tier, total games, recent match history

### 4. Naming Conventions
- Database: `snake_case` for tables/columns
- Python: `snake_case` for functions/variables, `PascalCase` for classes (e.g. FastAPI Pydantic models)
- JavaScript: `camelCase` for variables/functions
- API routes: plural nouns, REST-style (`/players`, not `/getPlayers`)

### 5. Wireframe Notes (keep it simple for v1)
- No need for pixel-perfect design — plain, clean HTML/CSS is fine. Prioritize clarity: big buttons for "Assign Next" and "Log Match" since these get used constantly during a live session.
- Mobile-friendly is worth it early, since you'll likely be running this from your phone courtside.
