"""Small migration script to add tags, event_date, event_time columns to notes table in SQLite.

Usage: run this once after pulling changes:
    python scripts/add_note_fields_migration.py

It will check if columns exist and add them if missing.
"""
import sqlite3
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'database', 'app.db')

if not os.path.exists(DB_PATH):
    print(f"Database not found at {DB_PATH}")
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# get current columns
cur.execute("PRAGMA table_info(note);")
cols = [r[1] for r in cur.fetchall()] if cur.description is not None else []
print("Existing columns:", cols)

# map of column -> SQL to add
to_add = {}
if 'tags' not in cols:
    to_add['tags'] = "ALTER TABLE note ADD COLUMN tags TEXT"
if 'position' not in cols:
    to_add['position'] = "ALTER TABLE note ADD COLUMN position INTEGER"
if 'event_date' not in cols:
    to_add['event_date'] = "ALTER TABLE note ADD COLUMN event_date DATE"
if 'event_time' not in cols:
    to_add['event_time'] = "ALTER TABLE note ADD COLUMN event_time TIME"

if not to_add:
    print("No migration necessary. All columns exist.")
else:
    for name, sql in to_add.items():
        try:
            print(f"Adding column {name}...")
            cur.execute(sql)
            conn.commit()
            print(f"Column {name} added.")
        except Exception as e:
            print(f"Failed to add {name}:", e)

conn.close()
print("Migration complete.")
