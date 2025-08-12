import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

# Import Django and configure
import django
django.setup()

# Import the WSGI application
from blog_project.wsgi import application

# Vercel handler
def handler(request, context):
    """Vercel serverless function handler"""
    return application(request, context)

# Alternative: direct app export for some Vercel configurations
app = application
