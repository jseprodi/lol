import os
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from io import BytesIO

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

# Set minimum required environment variables if not present
if 'SECRET_KEY' not in os.environ:
    os.environ['SECRET_KEY'] = 'django-insecure-development-key-change-in-production'
if 'DEBUG' not in os.environ:
    os.environ['DEBUG'] = 'True'
if 'VERCEL' not in os.environ:
    os.environ['VERCEL'] = 'True'

# Test database connection before Django setup
try:
    import psycopg2
    from urllib.parse import urlparse
    
    # Parse the DATABASE_URL
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        parsed = urlparse(db_url)
        # Test connection
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],  # Remove leading slash
            user=parsed.username,
            password=parsed.password
        )
        conn.close()
        print("Database connection successful")
    else:
        print("No DATABASE_URL found")
except Exception as e:
    print(f"Database connection failed: {e}")
    # Continue anyway, let Django handle the error

# Import Django and configure
import django
django.setup()

# Import Django components
from django.core.wsgi import get_wsgi_application

# Get the WSGI application
application = get_wsgi_application()

class VercelHandler(BaseHTTPRequestHandler):
    """Vercel-compatible HTTP request handler that bridges to Django"""
    
    def do_GET(self):
        """Handle GET requests"""
        self._handle_request('GET')
    
    def do_POST(self):
        """Handle POST requests"""
        self._handle_request('POST')
    
    def _handle_request(self, method):
        """Handle HTTP requests by bridging to Django"""
        try:
            # Parse the URL
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            
            # For now, let's test with a simple response to see if the handler works
            if path == '/':
                # Test database connection
                db_status = "Unknown"
                try:
                    import psycopg2
                    from urllib.parse import urlparse
                    
                    db_url = os.environ.get('DATABASE_URL')
                    if db_url:
                        parsed = urlparse(db_url)
                        conn = psycopg2.connect(
                            host=parsed.hostname,
                            port=parsed.port,
                            database=parsed.path[1:],
                            user=parsed.username,
                            password=parsed.password
                        )
                        conn.close()
                        db_status = "Connected successfully"
                    else:
                        db_status = "No DATABASE_URL"
                except Exception as e:
                    db_status = f"Connection failed: {str(e)}"
                
                response_html = f'''
                <h1>Hello from Vercel!</h1>
                <p>Handler is working.</p>
                <h2>Environment Check:</h2>
                <ul>
                    <li>SECRET_KEY: {"Set" if os.environ.get('SECRET_KEY') else "Missing"}</li>
                    <li>DATABASE_URL: {"Set" if os.environ.get('DATABASE_URL') else "Missing"}</li>
                    <li>VERCEL: {"Set" if os.environ.get('VERCEL') else "Missing"}</li>
                    <li>Database Status: {db_status}</li>
                </ul>
                <p><a href="/test-django">Test Django</a></p>
                '''
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(response_html.encode())
                return
            
            # Read request body for POST
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Create a file-like object for wsgi.input
            if content_length > 0:
                body_bytes = self.rfile.read(content_length)
                wsgi_input = BytesIO(body_bytes)
            else:
                wsgi_input = BytesIO(b'')
            
            # Create WSGI environment
            environ = {
                'REQUEST_METHOD': method,
                'PATH_INFO': path,
                'QUERY_STRING': parsed_url.query,
                'SERVER_NAME': 'vercel',
                'SERVER_PORT': '80',
                'HTTP_HOST': self.headers.get('Host', ''),
                'HTTP_USER_AGENT': self.headers.get('User-Agent', ''),
                'HTTP_ACCEPT': self.headers.get('Accept', ''),
                'CONTENT_TYPE': self.headers.get('Content-Type', ''),
                'CONTENT_LENGTH': content_length,
                'wsgi.input': wsgi_input,
                'wsgi.url_scheme': 'https',
                'wsgi.version': (1, 0),
                'wsgi.errors': sys.stderr,
                'wsgi.multithread': False,
                'wsgi.multiprocess': False,
                'wsgi.run_once': True,
            }
            
            # Create a start_response callable
            def start_response(status, headers, exc_info=None):
                status_code = int(status.split()[0])
                self.send_response(status_code)
                
                for header, value in headers:
                    self.send_header(header, value)
                self.end_headers()
                
                return self.wfile.write
            
            # Call Django WSGI application
            response_iterable = application(environ, start_response)
            
            # Write response content
            for chunk in response_iterable:
                if isinstance(chunk, bytes):
                    self.wfile.write(chunk)
                else:
                    self.wfile.write(chunk.encode('utf-8'))
            
            # Close response if needed
            if hasattr(response_iterable, 'close'):
                response_iterable.close()
                
        except Exception as e:
            import traceback
            error_details = f'Internal Server Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}'
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(error_details.encode())

# Vercel requires these exports
handler = VercelHandler
app = VercelHandler
