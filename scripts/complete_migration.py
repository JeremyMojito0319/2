"""
Complete migration guide for switching to Supabase

Step 1: Verify Supabase Connection
Step 2: Create Tables in Supabase  
Step 3: Migrate Data from SQLite
Step 4: Test Application
Step 5: Deploy to Vercel
"""

import os
import sys
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

load_dotenv()

def step1_verify_connection():
    """Step 1: Test Supabase connection"""
    print("🔍 Step 1: Verifying Supabase Connection")
    print("-" * 50)
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found. Please check your .env file.")
        return False
    
    try:
        import psycopg2
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        conn.close()
        print(f"✅ Connected to: {version[0][:60]}...")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Try these solutions:")
        print("   1. Check your Supabase project is active")
        print("   2. Verify the connection string in Supabase dashboard")
        print("   3. Check your internet connection")
        print("   4. Try using the connection pooler URL instead")
        return False

def step2_create_tables():
    """Step 2: Create tables in Supabase"""
    print("\n🏗️  Step 2: Creating Tables in Supabase")
    print("-" * 50)
    
    try:
        from src.models.user import db, User
        from src.models.note import Note
        from flask import Flask
        
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = 'migration-key'
        
        db.init_app(app)
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Tables created successfully!")
            
            # Verify tables exist
            from sqlalchemy import text
            result = db.session.execute(text("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"📊 Created tables: {tables}")
            
        return True
    except Exception as e:
        print(f"❌ Table creation failed: {e}")
        return False

def step3_migrate_data():
    """Step 3: Migrate data from SQLite"""
    print("\n📦 Step 3: Migrating Data from SQLite")
    print("-" * 50)
    
    sqlite_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'app.db')
    
    if not os.path.exists(sqlite_path):
        print("ℹ️  No SQLite database found. Skipping data migration.")
        return True
    
    try:
        from src.models.user import db, User
        from src.models.note import Note
        from flask import Flask
        
        # Setup Flask app
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = 'migration-key'
        
        db.init_app(app)
        
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        with app.app_context():
            # Migrate notes
            sqlite_cursor.execute("SELECT * FROM note")
            notes_data = sqlite_cursor.fetchall()
            
            sqlite_cursor.execute("PRAGMA table_info(note)")
            columns = [col[1] for col in sqlite_cursor.fetchall()]
            
            migrated_notes = 0
            for row in notes_data:
                note_dict = dict(zip(columns, row))
                
                # Handle datetime fields
                created_at = datetime.utcnow()
                updated_at = datetime.utcnow()
                
                if note_dict.get('created_at'):
                    try:
                        created_at = datetime.fromisoformat(note_dict['created_at'].replace('Z', '+00:00'))
                    except:
                        pass
                
                if note_dict.get('updated_at'):
                    try:
                        updated_at = datetime.fromisoformat(note_dict['updated_at'].replace('Z', '+00:00'))
                    except:
                        pass
                
                # Create new note
                note = Note(
                    title=note_dict.get('title', 'Untitled'),
                    content=note_dict.get('content', ''),
                    tags=note_dict.get('tags'),
                    position=note_dict.get('position'),
                    event_date=None,  # Handle date parsing if needed
                    event_time=None,  # Handle time parsing if needed
                    created_at=created_at,
                    updated_at=updated_at
                )
                
                db.session.add(note)
                migrated_notes += 1
            
            db.session.commit()
            print(f"✅ Migrated {migrated_notes} notes successfully!")
        
        sqlite_conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Data migration failed: {e}")
        return False

def step4_test_application():
    """Step 4: Test the application"""
    print("\n🧪 Step 4: Testing Application")
    print("-" * 50)
    
    try:
        from src.models.user import db, User
        from src.models.note import Note
        from flask import Flask
        
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = 'test-key'
        
        db.init_app(app)
        
        with app.app_context():
            # Test creating a note
            test_note = Note(
                title="Migration Test",
                content="This note confirms the migration was successful",
                tags="test,migration"
            )
            
            db.session.add(test_note)
            db.session.commit()
            
            # Test querying notes
            notes = Note.query.all()
            print(f"✅ Found {len(notes)} notes in Supabase")
            
            # Clean up test note
            db.session.delete(test_note)
            db.session.commit()
            
        return True
        
    except Exception as e:
        print(f"❌ Application test failed: {e}")
        return False

def main():
    """Run the complete migration process"""
    print("🚀 Supabase Migration Process")
    print("=" * 50)
    
    steps = [
        ("Verify Connection", step1_verify_connection),
        ("Create Tables", step2_create_tables), 
        ("Migrate Data", step3_migrate_data),
        ("Test Application", step4_test_application)
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Migration stopped at: {step_name}")
            print("\nPlease fix the issue and run the script again.")
            return False
    
    print("\n🎉 Migration Complete!")
    print("=" * 50)
    print("✅ Your application is now using Supabase!")
    print("\nNext steps:")
    print("1. Test your app: python src/main.py")
    print("2. Deploy to Vercel with these environment variables:")
    print("   - DATABASE_URL")
    print("   - GITHUB_TOKEN") 
    print("   - SUPABASE_URL")
    print("   - SUPABASE_KEY")
    print("   - SECRET_KEY")
    
    return True

if __name__ == "__main__":
    main()