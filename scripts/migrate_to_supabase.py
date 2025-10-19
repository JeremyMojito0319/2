"""
Migration script to create tables in Supabase and optionally migrate data from SQLite.

Usage:
    python scripts/migrate_to_supabase.py

This script will:
1. Create the necessary tables in Supabase
2. Optionally migrate existing data from SQLite (if app.db exists)
"""

import os
import sys
import sqlite3
from dotenv import load_dotenv

# Add the parent directory to the path so we can import our models
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

load_dotenv()

# Import after setting up the path
from src.models.user import db, User
from src.models.note import Note
from flask import Flask

def create_app():
    """Create Flask app with Supabase configuration"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'migration-key'
    
    # Use Supabase PostgreSQL
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required for Supabase migration")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    return app

def migrate_data_from_sqlite():
    """Migrate existing data from SQLite to Supabase"""
    sqlite_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'app.db')
    
    if not os.path.exists(sqlite_path):
        print("No SQLite database found. Skipping data migration.")
        return
    
    print("Found existing SQLite database. Migrating data...")
    
    # Connect to SQLite
    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_cursor = sqlite_conn.cursor()
    
    try:
        # Check what tables exist in SQLite
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in sqlite_cursor.fetchall()]
        print(f"Found tables in SQLite: {tables}")
        
        # Migrate users if table exists
        if 'user' in tables:
            sqlite_cursor.execute("SELECT * FROM user")
            users_data = sqlite_cursor.fetchall()
            
            # Get column names
            sqlite_cursor.execute("PRAGMA table_info(user)")
            user_columns = [col[1] for col in sqlite_cursor.fetchall()]
            print(f"User columns: {user_columns}")
            
            for row in users_data:
                user_data = dict(zip(user_columns, row))
                user = User(
                    username=user_data.get('username'),
                    email=user_data.get('email')
                )
                db.session.add(user)
            
            print(f"Migrated {len(users_data)} users")
        
        # Migrate notes if table exists
        if 'note' in tables:
            sqlite_cursor.execute("SELECT * FROM note")
            notes_data = sqlite_cursor.fetchall()
            
            # Get column names
            sqlite_cursor.execute("PRAGMA table_info(note)")
            note_columns = [col[1] for col in sqlite_cursor.fetchall()]
            print(f"Note columns: {note_columns}")
            
            for row in notes_data:
                note_data = dict(zip(note_columns, row))
                
                # Handle datetime conversion
                from datetime import datetime
                created_at = None
                updated_at = None
                
                if note_data.get('created_at'):
                    try:
                        created_at = datetime.fromisoformat(note_data['created_at'].replace('Z', '+00:00'))
                    except:
                        created_at = datetime.utcnow()
                
                if note_data.get('updated_at'):
                    try:
                        updated_at = datetime.fromisoformat(note_data['updated_at'].replace('Z', '+00:00'))
                    except:
                        updated_at = datetime.utcnow()
                
                # Handle date/time fields
                event_date = None
                event_time = None
                
                if note_data.get('event_date'):
                    try:
                        from datetime import date
                        event_date = date.fromisoformat(note_data['event_date'])
                    except:
                        pass
                
                if note_data.get('event_time'):
                    try:
                        from datetime import time
                        event_time = time.fromisoformat(note_data['event_time'])
                    except:
                        pass
                
                note = Note(
                    title=note_data.get('title', 'Untitled'),
                    content=note_data.get('content', ''),
                    tags=note_data.get('tags'),
                    position=note_data.get('position'),
                    event_date=event_date,
                    event_time=event_time,
                    created_at=created_at,
                    updated_at=updated_at
                )
                db.session.add(note)
            
            print(f"Migrated {len(notes_data)} notes")
        
        # Commit all changes
        db.session.commit()
        print("Data migration completed successfully!")
        
    except Exception as e:
        print(f"Error during data migration: {e}")
        db.session.rollback()
        raise
    finally:
        sqlite_conn.close()

def main():
    """Main migration function"""
    print("Starting Supabase migration...")
    
    # Create Flask app and application context
    app = create_app()
    
    with app.app_context():
        print("Creating tables in Supabase...")
        
        # Drop all tables and recreate (be careful in production!)
        # db.drop_all()
        
        # Create all tables
        db.create_all()
        print("Tables created successfully!")
        
        # Migrate existing data
        migrate_data_from_sqlite()
    
    print("Migration completed!")
    print("\nNext steps:")
    print("1. Test your application with: python src/main.py")
    print("2. Verify data in Supabase dashboard")
    print("3. Update your .env file to use DATABASE_URL for production")

if __name__ == '__main__':
    main()