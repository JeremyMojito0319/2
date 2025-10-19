"""
Minimal Vercel-compatible Flask app
"""
import os
import sys

# Ensure we can import everything
try:
    from flask import Flask
    from flask_cors import CORS
    print("✓ Flask imports successful")
except ImportError as e:
    print(f"✗ Flask import error: {e}")
    sys.exit(1)

# Try to create a minimal app
try:
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/')
    def hello():
        return {"message": "Hello from Vercel!"}
    
    @app.route('/api/health')
    def health():
        return {"status": "ok"}
    
    print("✓ Minimal Flask app created successfully")
    print(f"✓ App type: {type(app)}")
    
except Exception as e:
    print(f"✗ Error creating Flask app: {e}")
    sys.exit(1)

# This is what Vercel will import
# No additional functions or classes that might confuse Vercel
if __name__ == "__main__":
    app.run(debug=True)