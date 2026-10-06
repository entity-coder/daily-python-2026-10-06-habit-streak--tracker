# 🌱 Habit Streak Tracker

A small command-line tool to build consistent habits. Add a habit, check it in
each day, and watch your streak grow — nothing fancy, just a JSON file and the
standard library.

## What it does

- **Track habits**: add habits you want to build ("Read 20 minutes", "Exercise", …)
- **Daily check-ins**: mark a habit done for today with one command
- **Streaks**: see your current streak per habit (a streak survives if you haven't checked in today yet — it only counts completed days backwards)
- **Weekly summary**: a 7-day ✅/⬜ grid per habit plus total check-ins

## Features

- Zero dependencies — Python 3.10+ standard library only
- Case-insensitive habit names
- Data stored in a readable `habits.json` next to the script (you can back it up or sync it yourself)
- Friendly streak fire 🔥 for streaks of 7+ days

## How to run

```bash
# Start tracking a habit
python habit_tracker.py add "Read 20 minutes"

# Check it in for today
python habit_tracker.py done "Read 20 minutes"

# See all current streaks
python habit_tracker.py streaks

# 7-day overview grid
python habit_tracker.py summary

# Stop tracking a habit
python habit_tracker.py remove "Read 20 minutes"
```

Example output of `streaks`:

```
Habit                         Streak  Today
--------------------------------------------------
Exercise                      12      ✅ 🔥
Read 20 minutes               3       ✅
```

## Requirements

- Python 3.10 or newer (no packages to install)

## Interview notes

**What this is:** a zero-dependency CLI habit tracker — add habits, check in daily, see streaks and a weekly overview. Built as a "do one thing well" command-line tool.

**Why these choices:**
- **Standard library only (no pip install):** the tool needs arg parsing, JSON I/O, and date math — all covered by `argparse`, `json`, `datetime`, and `pathlib`. No dependencies means it runs on any machine with Python 3.10+ and there's nothing to break on upgrade.
- **JSON file instead of SQLite:** for a single-user CLI, a readable `habits.json` next to the script is the right size — the user can inspect, back up, or sync it by hand. A database would add setup with no real benefit at this scale.
- **Check-ins stored as ISO date strings** (`"2026-10-06"`) in a list: trivially sortable and comparable, human-readable in the file, and timezone-naive by design (a "day" is the user's local day).
- **Streak counts backwards from yesterday if today isn't checked in yet:** a streak measures completed days, so an unchecked today doesn't zero it — it only breaks when a full day is missed. That was the main edge case in the streak logic (`current_streak`).
- **Case-insensitive habit names:** a small UX decision so `"Read 20 minutes"` and `"read 20 minutes"` don't silently become two habits.

**Trade-offs I'd mention honestly:**
- No file locking on `habits.json` — fine for one person, would risk corruption under concurrent writes; a multi-user version would need SQLite or locks.
- Dates are local-time naive; crossing timezones mid-streak could miscount a day.
- No reminders, no history editing, no non-daily frequencies — deliberately out of scope for v1.

**How I'd extend it:** scheduled reminders (cron or desktop notification), weekly/non-daily habit frequencies, a `--json` flag for scripting, and rest-day / streak-freeze support.

*Part of a daily portfolio series — one small project every day.*
