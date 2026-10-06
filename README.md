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
