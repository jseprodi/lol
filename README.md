# Django Blog

A modern, feature-rich blog built with Django 5.2. This blog includes categories, tags, comments, search functionality, and a beautiful responsive design.

## Features

- **Modern Design**: Clean, responsive design using Bootstrap 5
- **Content Management**: Full admin interface for managing posts, categories, and tags
- **Search Functionality**: Search posts by title, content, or excerpt
- **Categories & Tags**: Organize content with categories and tags
- **Comments System**: Allow readers to comment on posts
- **Pagination**: Navigate through posts with pagination
- **Related Posts**: Show related posts based on categories
- **View Tracking**: Track post views
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile

## Technology Stack

- **Backend**: Django 5.2
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: Bootstrap 5, Font Awesome
- **Image Handling**: Pillow
- **Styling**: Custom CSS

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd blog2
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Blog: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## Project Structure

```
blog2/
├── blog/                    # Blog application
│   ├── migrations/         # Database migrations
│   ├── templates/blog/     # Blog templates
│   ├── admin.py           # Admin configuration
│   ├── models.py          # Database models
│   ├── urls.py            # URL routing
│   └── views.py           # View functions
├── blog_project/          # Main project settings
│   ├── settings.py        # Django settings
│   └── urls.py           # Main URL configuration
├── templates/             # Base templates
├── static/               # Static files (CSS, JS, images)
├── media/               # User-uploaded files
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## Models

### Post
- Title, slug, content, excerpt
- Author, category, tags
- Status (draft/published)
- Published date, view count
- Featured image

### Category
- Name, slug, description
- Related posts

### Tag
- Name, slug
- Related posts

### Comment
- Name, email, body
- Related to posts
- Active/inactive status

## Admin Interface

The Django admin interface provides full control over:
- Creating and editing posts
- Managing categories and tags
- Moderating comments
- User management

## Customization

### Adding New Features
1. Create new models in `blog/models.py`
2. Add views in `blog/views.py`
3. Create templates in `templates/blog/`
4. Update URLs in `blog/urls.py`

### Styling
- Main styles: `static/css/style.css`
- Bootstrap 5 for responsive design
- Font Awesome for icons

### Configuration
- Database settings: `blog_project/settings.py`
- Static and media files configuration included
- Debug mode enabled for development

## Deployment

For production deployment:

1. **Set DEBUG = False** in settings.py
2. **Configure a production database** (PostgreSQL recommended)
3. **Set up static file serving** (nginx/Apache)
4. **Configure media file storage**
5. **Set up environment variables** for SECRET_KEY
6. **Use a production WSGI server** (Gunicorn/uWSGI)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please open an issue on the repository. 