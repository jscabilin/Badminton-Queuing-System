# Product Requirements Document (PRD)
## Badminton Queue & Fair-Play System

### 1. Overview
A web app that helps badminton organizers run fair, well-managed play sessions. It queues players onto a fixed number of courts, tracks how many games each player has played (so no one is stuck on the bench or hogging a court), categorizes players by skill level, and — over time — suggests when a player should be promoted to a higher skill tier based on real match results.

This is a personal learning project. It's meant to be genuinely useful for real sessions, and also a vehicle for growing as a developer (frontend, backend, database design, and eventually basic ML).

### 2. Problem Statement
Badminton group sessions are usually organized manually — a whiteboard, a notebook, or someone's memory. This leads to:
- Some players playing far more games than others (unfair rotation)
- No consistent way to track skill level, so pairings/matchups feel random
- No record of how a player is actually performing, so skill categorization stays static even as players improve

### 3. Goals
- Let an organizer create a **session** (a specific date/venue/group of players) with a fixed number of courts
- Maintain a **fair queue**: players with fewer games played get prioritized for the next open court
- Let organizers **tag players** into skill categories: Beginner, Lower Intermediate, Higher Intermediate, Advance
- Track **match history** per player (who they played, what tier those opponents were, win/loss)
- **Suggest level-ups** automatically based on rule-based performance patterns (e.g., a Beginner who repeatedly performs well against Lower/Higher Intermediate players gets flagged for review)
- Support **multiple groups/sessions** — this isn't hardcoded to one venue or one barkada
- Let players **view their own stats and queue position** (read-only for v1)

### 4. Non-Goals (v1)
- Players self-checking in or editing their own profile (organizer manages this for now)
- Real-time multi-device sync mid-session (polling/refresh is fine for v1)
- A trained ML model (v1 uses rule-based logic; ML is a planned future phase — see PLAN.md)
- Payments, court booking/reservations, tournament bracket generation

### 5. Target Users
- **Organizer/Admin** (you, and eventually other group organizers): creates sessions, manages players, assigns courts, reviews level-up suggestions
- **Player**: views their own play count, current queue position, and skill tier

### 6. Core Features (Functional Requirements)

| # | Feature | Description |
|---|---|---|
| F1 | Player Management | Create/edit players, assign initial skill tag (Beginner → Advance) |
| F2 | Session Management | Create a session with a name, date, and number of courts |
| F3 | Fair Queue Engine | Auto-assign the next 4 lowest-play-count players to an open court |
| F4 | Match Recording | Log match results (players involved, winner/loser or score, court, timestamp) |
| F5 | Play Count Tracking | Every player's total games-played updates automatically per match logged |
| F6 | Skill Categorization | Players belong to one of 4 tiers; tier is stored and historized (so you can see tier changes over time) |
| F7 | Level-Up Suggestion Engine | Rule-based logic flags a player as "consider promoting" based on match results vs higher-tier opponents (see RULES.md) |
| F8 | Player Self-View | A player can look up their own stats: games played, current tier, queue position, recent matches |
| F9 | Multi-Session/Group Support | Data model supports many independent groups/sessions, not just one |

### 7. User Stories
- *As an organizer*, I want to add players and tag their skill level, so I can start a session quickly.
- *As an organizer*, I want the system to tell me who should play next, so nobody is stuck waiting too long.
- *As an organizer*, I want to log match results quickly between games, so play counts stay accurate.
- *As an organizer*, I want to see a "this player might be ready to level up" suggestion, so I can make an informed call instead of guessing.
- *As a player*, I want to check how many games I've played and what tier I'm in, so I understand my standing in the group.

### 8. Success Criteria (v1)
- An organizer can run a full real-life session end-to-end using only this app (no whiteboard needed)
- Play counts are visibly fairer than manual tracking (lower variance in games-played per player by end of session)
- At least one real level-up suggestion is generated and feels "reasonable" to the organizer

### 9. Open Questions (revisit as you build)
- What counts as "performed well" against a higher tier — win, close loss, or organizer's manual judgment call too?
- Should a level-up suggestion require organizer approval before it changes the player's tier? (Recommended: yes, for v1 — keep a human in the loop.)
