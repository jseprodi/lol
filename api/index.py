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

# Import Django components
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.conf import settings

# Get the WSGI application
application = get_wsgi_application()

# Vercel requires these exports
app = application
handler = application
