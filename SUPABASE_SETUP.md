# Supabase Setup Guide for Django Blog

This guide will help you set up Supabase as your PostgreSQL database for the Django blog project.

## 1. Create a Supabase Account

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project" and sign up
3. Create a new organization and project

## 2. Get Your Database Connection String

1. In your Supabase dashboard, go to **Settings** → **Database**
2. Find the **Connection string** section
3. Copy the **URI** connection string
4. It will look like: `postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres`

## 3. Set Up Environment Variables

### For Local Development:
Create a `.env` file in your project root:
```bash
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
SECRET_KEY=your-secret-key-here
DEVELOPMENT=True
```

### For Vercel Deployment:
1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add the following variables:
   - `DATABASE_URL`: Your Supabase connection string
   - `SECRET_KEY`: A secure secret key for Django

## 4. Update Django Settings

The project is already configured to automatically use Supabase when `DATABASE_URL` is present in environment variables.

## 5. Run Migrations

After setting up your environment variables:

```bash
# Activate virtual environment
venv\Scripts\activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## 6. Test the Connection

1. Start your Django server: `python manage.py runserver`
2. Go to http://127.0.0.1:8000/admin/
3. Log in with your superuser credentials
4. Create some test categories, tags, and posts

## 7. Deploy to Vercel

1. Push your changes to GitHub
2. Deploy using Vercel CLI: `vercel`
3. Set environment variables in Vercel dashboard
4. Your blog will now use Supabase in production!

## Important Notes

- **Never commit your `.env` file** (it's already in `.gitignore`)
- **Keep your database credentials secure**
- **Supabase free tier includes**: 500MB database, 2GB bandwidth, 50MB file storage
- **Database backups**: Supabase automatically backs up your data

## Troubleshooting

### Connection Issues:
- Verify your connection string format
- Check if your IP is allowed in Supabase dashboard
- Ensure your database password is correct

### Migration Issues:
- If you get table errors, you may need to drop and recreate the database
- Use `python manage.py migrate --run-syncdb` if needed

## Support

- [Supabase Documentation](https://supabase.com/docs)
- [Django Database Documentation](https://docs.djangoproject.com/en/5.2/ref/databases/)
- [Vercel Documentation](https://vercel.com/docs)
