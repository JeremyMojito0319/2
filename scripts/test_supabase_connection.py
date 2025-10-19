"""
Test script to verify Supabase connection
"""
import os
import sys
from dotenv import load_dotenv
import psycopg2

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

load_dotenv()

def test_connection():
    """Test connection to Supabase PostgreSQL"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    print(f"🔄 Testing connection to: {database_url[:50]}...")
    
    try:
        # Test direct connection
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Connected to PostgreSQL: {version[0][:80]}...")
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        print(f"📊 Found {len(tables)} tables: {[t[0] for t in tables]}")
        
        conn.close()
        print("✅ Database connection test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()