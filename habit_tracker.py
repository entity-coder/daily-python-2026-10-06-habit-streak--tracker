#!/usr/bin/env python3
"""
Habit Streak Tracker
====================
A tiny CLI tool that helps you build consistent habits by tracking daily
check-ins and computing streaks (consecutive days a habit was completed).

Usage:
    python habit_tracker.py add "Read 20 minutes"          # add a new habit
    python habit_tracker.py done "Read 20 minutes"         # check in for today
    python habit_tracker.py streaks                        # show all streaks
    python habit_tracker.py summary                        # 7-day overview
    python habit_tracker.py remove "Read 20 minutes"       # delete a habit

Data is stored in a JSON file (default: habits.json) next to the script,
so nothing extra needs to be installed.
"""

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

DATA_FILE = Path(__file__).with_name("habits.json")
TODAY = date.today().isoformat()


def load_data() -> dict:
    """Load the habits file; return an empty structure if it doesn't exist."""
    if not DATA_FILE.exists():
        return {"habits": {}}
    with DATA_FILE.open() as f:
        return json.load(f)


def save_data(data: dict) -> None:
    """Write habits back to disk, pretty-printed for readability."""
    with DATA_FILE.open("w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def find_habit(data: dict, name: str) -> str | None:
    """Case-insensitive lookup so 'Read 20 minutes' matches 'read 20 minutes'."""
    for key in data["habits"]:
        if key.lower() == name.lower():
            return key
    return None


def cmd_add(data: dict, name: str) -> None:
    if find_habit(data, name):
        print(f'"{name}" is already being tracked.')
        return
    data["habits"][name.strip()] = {"created": TODAY, "checkins": []}
    save_data(data)
    print(f'Now tracking "{name.strip()}". Day one starts today! 🌱')


def cmd_done(data: dict, name: str) -> None:
    key = find_habit(data, name)
    if key is None:
        print(f'No habit named "{name}". Add it first with: add')
        return
    checkins = data["habits"][key]["checkins"]
    if TODAY in checkins:
        print(f'"{key}" is already checked in for today. Keep going! ✅')
        return
    checkins.append(TODAY)
    checkins.sort()
    save_data(data)
    streak = current_streak(checkins)
    print(f'Logged "{key}" for {TODAY}. Current streak: {streak} day(s) 🔥')


def current_streak(checkins: list[str]) -> int:
    """Count consecutive days ending today (or yesterday, to not break a streak)."""
    days = set(checkins)
    streak, cursor = 0, date.today()
    if cursor.isoformat() not in days:  # hasn't checked in today yet
        cursor -= timedelta(days=1)
    while cursor.isoformat() in days:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def cmd_streaks(data: dict) -> None:
    if not data["habits"]:
        print("No habits yet. Add one with: add \"<name>\"")
        return
    print(f"{'Habit':<30}{'Streak':<8}Today")
    print("-" * 50)
    for name, info in sorted(data["habits"].items()):
        streak = current_streak(info["checkins"])
        today_done = "✅" if TODAY in info["checkins"] else "⬜"
        fire = " 🔥" if streak >= 7 else ""
        print(f"{name:<30}{streak:<8}{today_done}{fire}")


def cmd_summary(data: dict) -> None:
    """Show a 7-day grid: rows = habits, columns = days, ✅/⬜ = done/missed."""
    if not data["habits"]:
        print("No habits yet. Add one with: add \"<name>\"")
        return
    week = [(date.today() - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
    header = "Habit".ljust(26) + " ".join(d[5:] for d in week)  # MM-DD columns
    print(header)
    for name, info in sorted(data["habits"].items()):
        days = set(info["checkins"])
        row = " ".join("✅" if d in days else "⬜" for d in week)
        print(f"{name[:25].ljust(26)}{row}")
    print(f"\nTotal check-ins this week: {sum(1 for info in data['habits'].values() for d in info['checkins'] if d in week)}")


def cmd_remove(data: dict, name: str) -> None:
    key = find_habit(data, name)
    if key is None:
        print(f'No habit named "{name}".')
        return
    del data["habits"][key]
    save_data(data)
    print(f'Stopped tracking "{key}".')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Track daily habits and keep your streaks alive."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="start tracking a new habit")
    p_add.add_argument("name", help="name of the habit, e.g. \"Read 20 minutes\"")

    p_done = sub.add_parser("done", help="check in a habit for today")
    p_done.add_argument("name", help="name of the habit")

    sub.add_parser("streaks", help="show current streaks for all habits")
    sub.add_parser("summary", help="show a 7-day check-in grid")

    p_rm = sub.add_parser("remove", help="stop tracking a habit")
    p_rm.add_argument("name", help="name of the habit")

    args = parser.parse_args(argv)
    data = load_data()

    if args.command == "add":
        cmd_add(data, args.name)
    elif args.command == "done":
        cmd_done(data, args.name)
    elif args.command == "streaks":
        cmd_streaks(data)
    elif args.command == "summary":
        cmd_summary(data)
    elif args.command == "remove":
        cmd_remove(data, args.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
