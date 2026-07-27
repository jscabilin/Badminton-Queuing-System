# Rules Document
## Badminton Queue & Fair-Play System

This document defines the actual business logic — the "brain" of the app. Keep this file updated as you tune the rules; it should always reflect what the code actually does.

### 1. Fair Queue Rules

**Goal:** minimize the gap between the most-played and least-played player during a session.

- Players waiting are sorted by `total_games_played` (ascending) — lowest play count goes first.
- **Tie-breaker 1:** longest time since their last match ended.
- **Tie-breaker 2:** order joined the session (first added, first served).
- When a court opens up, the top N players (2 for singles, 4 for doubles) are auto-assigned.
- A player currently on a court is removed from the waiting pool until their match is logged as finished.

**Edge cases:**
- **Odd number of waiting players for doubles:** hold the last player until one more is available, or offer organizer a manual override to form a mixed/singles match.
- **No-show/skip:** organizer can mark a player "sit out" for one rotation without incrementing their play count — they don't lose fairness priority for the round they intentionally skip.

### 2. Skill Tier Rules

Four tiers, in order: `beginner` → `lower_intermediate` → `higher_intermediate` → `advance`

- A player's **initial tier** is self-tagged or organizer-assigned when added.
- Tier changes are **never automatic** — the system only ever *suggests*. An organizer must approve a change (see `promotion_suggestions` table in DESIGN.md). This keeps a human judgment call in the loop, since skill assessment is inherently subjective.

### 3. Promotion Suggestion Rules (v1 — rule-based)

A promotion suggestion is generated when **all** of the following are true for a player, evaluated after each match is logged:

1. Player has played at least **5 matches** total (avoid suggesting off tiny sample size).
2. Within their **last 10 matches**, they have **won at least 3 matches** against opponents whose `opponent_tier` (snapshot at match time) is **one tier above** their current tier.
3. No existing `pending` suggestion already exists for that player (avoid duplicate spam).

When triggered:
- Create a row in `promotion_suggestions` with `suggested_tier` = next tier up, and a `reason_summary` like: "Won 3 of last 10 vs Higher Intermediate opponents."
- Suggestion stays `pending` until the organizer approves or dismisses it.
- If **dismissed**, don't re-suggest for the same tier until at least 5 more matches have been played (avoid nagging).

**Not in v1 (intentionally left simple for now):**
- No demotion logic yet (a player who loses a lot doesn't get auto-flagged down). Add this later if it proves useful.
- No weighting by score margin (a 21-2 win counts the same as a 21-19 win). This is the first place to improve once you move toward the ML phase.

### 4. Future Rule Evolution (toward ML)
When you're ready to move past pure rules (see PLAN.md Phase 5), the `suggest_promotion()` function's *interface* stays the same — it still takes a player's match history and returns a suggestion + reason. What changes internally is *how* that decision is made (e.g., a simple statistical model considering score margin, opponent tier, and recency instead of a fixed "3 of last 10" threshold). Keep logging rich match data now (scores, not just win/loss) so you have good training data later even though v1 doesn't use it yet.

### 5. Data Integrity Rules
- A match must always reference a valid session and court.
- `opponent_tier` is captured **at the time of the match**, not looked up later — tiers change over time, and promotion logic depends on knowing what tier someone actually was when the match happened.
- A player cannot be in two matches on two different courts at the same time within a session.
