"""
Step-by-step guide to switch from SQLite to Supabase

Follow these steps in order:
"""

print("""
╔══════════════════════════════════════════════════════════════╗
║  SQLite → Supabase Migration Guide                          ║
╚══════════════════════════════════════════════════════════════╝

📋 Prerequisites Checklist:
  ✓ Supabase account created
  ✓ Supabase project created  
  ✓ Tables created in Supabase (users, notes)
  ✓ .env file configured with DATABASE_URL
  ✓ psycopg2-binary installed

🔧 Step 1: Test Supabase Connection
───────────────────────────────────────────────────────────────
Run this command to test your Supabase connection:

  conda activate software
  python scripts/test_supabase_connection.py

This will verify that:
  • Your DATABASE_URL is correct
  • Connection to Supabase works
  • Tables exist in the database

───────────────────────────────────────────────────────────────

📦 Step 2: Backup SQLite Data (Optional but Recommended)
───────────────────────────────────────────────────────────────
Create a backup of your SQLite database:

  copy database\\app.db database\\app.db.backup

───────────────────────────────────────────────────────────────

🚀 Step 3: Run Migration Script
───────────────────────────────────────────────────────────────
Migrate your data from SQLite to Supabase:

  conda activate software
  python scripts/migrate_to_supabase.py

This will:
  • Read all data from SQLite database
  • Transfer users and notes to Supabase
  • Update sequence numbers
  • Verify the migration

───────────────────────────────────────────────────────────────

✅ Step 4: Test the Application
───────────────────────────────────────────────────────────────
Start your application with Supabase:

  conda activate software
  python -m src.main

Then open http://localhost:5001 and verify:
  • All notes are visible
  • You can create new notes
  • You can edit existing notes
  • You can delete notes
  • Search functionality works

───────────────────────────────────────────────────────────────

🧪 Step 5: Test Database Switch
───────────────────────────────────────────────────────────────
Optional: Verify you can switch between databases:

  conda activate software
  python scripts/test_database_switch.py

───────────────────────────────────────────────────────────────

🎉 You're Done!
───────────────────────────────────────────────────────────────
Your application is now using Supabase PostgreSQL!

To switch back to SQLite (for local dev), simply:
  • Comment out DATABASE_URL in .env
  • Restart the application

The app will automatically fall back to SQLite.

═══════════════════════════════════════════════════════════════
""")
