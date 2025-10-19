"""
Simple script to test database switching between SQLite and PostgreSQL/Supabase
"""
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

load_dotenv()

def main():
    """Test the database configuration switching"""
    print("🔍 Database Configuration Test")
    print("=" * 50)
    
    # Check environment variables
    database_url = os.environ.get('DATABASE_URL')
    supabase_url = os.environ.get('SUPABASE_URL')
    github_token = os.environ.get('GITHUB_TOKEN')
    
    print(f"DATABASE_URL: {'✅ Set' if database_url else '❌ Not set'}")
    print(f"SUPABASE_URL: {'✅ Set' if supabase_url else '❌ Not set'}")
    print(f"GITHUB_TOKEN: {'✅ Set' if github_token else '❌ Not set'}")
    
    # Import Flask app components
    try:
        from src.models.user import db
        from src.models.note import Note
        from flask import Flask
        
        print("\n🏗️  Creating Flask app...")
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'test-key'
        
        if database_url:
            print(f"🐘 Using PostgreSQL/Supabase: {database_url[:50]}...")
            app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        else:
            print("🗄️  Using SQLite (local development)")
            ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            DB_PATH = os.path.join(ROOT_DIR, 'database', 'app.db')
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
            print(f"   Database path: {DB_PATH}")
        
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Initialize database
        db.init_app(app)
        
        with app.app_context():
            print("\n🔧 Testing database connection...")
            
            # Try to create tables
            db.create_all()
            print("✅ Tables created successfully!")
            
            # Test creating a sample note
            test_note = Note(
                title="Test Note",
                content="This is a test note to verify database connectivity",
                tags="test,verification"
            )
            
            db.session.add(test_note)
            db.session.commit()
            
            # Verify the note was created
            notes = Note.query.all()
            print(f"✅ Notes in database: {len(notes)}")
            
            # Clean up test note
            db.session.delete(test_note)
            db.session.commit()
            
            print("✅ Database test completed successfully!")
            
            return True
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 Next Steps:")
        print("1. To use SQLite: Keep DATABASE_URL commented out in .env")
        print("2. To use Supabase: Uncomment DATABASE_URL in .env") 
        print("3. Run: python src/main.py")
    else:
        print("\n💡 Check your database configuration and try again")