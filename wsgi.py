"""
WSGI entry point for Vercel deployment
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app

# WSGI application
application = app

if __name__ == "__main__":
    app.run()