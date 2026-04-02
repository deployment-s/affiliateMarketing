# Production Deployment Guide (Supabase)

## Overview

This Django ecommerce project is configured to use:
- **Supabase PostgreSQL** for database (requires IPv6 connectivity)
- **Supabase Storage** (S3-compatible) for product images and media files
- **Local SQLite** for development (to avoid IPv6 connectivity issues during dev)

## Pre-Deployment Checklist

### 1. Supabase Setup

#### Database
- [ ] Create Supabase project
- [ ] Note your **Project Reference** (e.g., `ityswbjguqeadyabvqrb`)
- [ ] Get **Database Connection String** from Supabase → Project Settings → Database
  - Format: `postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres`
- [ ] Ensure your production server has IPv6 connectivity enabled

#### Storage
- [ ] Create a storage bucket in Supabase → Storage (e.g., `products` or `media`)
- [ ] Set bucket permissions (public or private with signed URLs)
- [ ] Get **S3 Credentials** from Supabase → Project Settings → API → `s3` section:
  - Access Key ID
  - Secret Access Key
  - Region (usually `eu-west-1` or your project's region)

### 2. Environment Variables for Production

Create a `.env` file in production with these values:

```bash
# Django
SECRET_KEY=your-secure-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Supabase Database (PostgreSQL)
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.ityswbjguqeadyabvqrb.supabase.co:5432/postgres

# Supabase Storage (S3-compatible)
AWS_ACCESS_KEY_ID=your-s3-access-key
AWS_SECRET_ACCESS_KEY=your-s3-secret-key
AWS_STORAGE_BUCKET_NAME=products
AWS_S3_REGION_NAME=eu-west-1
AWS_S3_ENDPOINT_URL=https://ityswbjguqeadyabvqrb.supabase.co/storage/v1/s3
AWS_S3_CUSTOM_DOMAIN=https://ityswbjguqeadyabvqrb.supabase.co/storage/v1/object/public/products
AWS_QUERYSTRING_AUTH=False
AWS_S3_ADDRESSING_STYLE=path

DEFAULT_FILE_STORAGE=storages.backends.s3boto3.S3Boto3Storage
STATICFILES_STORAGE=storages.backends.s3boto3.S3Boto3Storage

# Static & Media URLs (optional but recommended)
MEDIA_URL=https://ityswbjguqeadyabvqrb.supabase.co/storage/v1/object/public/products/
STATIC_URL=https://ityswbjguqeadyabvqrb.supabase.co/storage/v1/object/public/products/

# Email Configuration (OPTIONAL - comment out to disable email)
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
# DEFAULT_FROM_EMAIL=your-email@gmail.com
# EMAIL_USE_TLS=True

# Stripe Configuration (OPTIONAL - comment out to disable payments)
# STRIPE_API_KEY_PUBLISHABLE=pk_live_...
# STRIPE_API_KEY_HIDDEN=sk_live_...
# STRIPE_SUCCESS_URL=https://yourdomain.com/success/
# STRIPE_CANCEL_URL=https://yourdomain.com/cancel/
```

**Important:**
- Generate a new `SECRET_KEY` for production (use `openssl rand -hex 32` or Django's `get_random_secret_key()`)
- Set `DEBUG=False`
- Add your actual domain to `ALLOWED_HOSTS`
- Email and Stripe are **optional** - omit them to disable those features

### 3. Deployment Steps

#### On your production server:

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd affiliateMarketing

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Install and build frontend assets
cd theme/static_src
npm install
npm run build
cd ..

# 5. Copy production .env file
# (upload your .env file to the server in the project root)

# 6. Apply migrations to Supabase
python manage.py migrate

# 7. Create superuser (optional)
python manage.py createsuperuser

# 8. Collect static files to S3 bucket
python manage.py collectstatic --noinput

# 9. Run the server (development) or configure for production WSGI/ASGI
python manage.py runserver  # For testing only
```

### 4. Production Server Configuration

For production, use **Gunicorn** (already in requirements.txt) with **Nginx**:

**Gunicorn command:**
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

**Nginx configuration** (example):
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        # Static files served from S3, but Django may need to serve some
        alias /path/to/your/static/files/;
    }

    location /media/ {
        # Media files served from S3 via custom domain
        # May not need local serving if using S3 directly
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

### 5. IPv6 Connectivity Requirement

**Critical:** Your production server must have IPv6 connectivity to connect to Supabase's database.

**Check IPv6:**
```bash
ping6 db.ityswbjguqeadyabvqrb.supabase.co
```

If IPv6 is not enabled:
- Contact your hosting provider to enable IPv6
- Use a VPS that supports IPv6 (DigitalOcean, Linode, AWS, etc. all have IPv6)
- For local testing without IPv6, you can only use Supabase Storage (images), not database

### 6. Important Notes

- **Static files** and **media files** will be uploaded to your Supabase bucket automatically via Django's storage backend
- The `products` bucket should be **public** or configure signed URLs
- The `AWS_S3_CUSTOM_DOMAIN` should point to your actual bucket public URL
- Thumbnails are generated on upload and stored in the same bucket
- **Security**: In production, use environment variables for all secrets, never commit `.env` to git
- **Migrations**: Always run `python manage.py migrate` after deploying to production
- **Backups**: Set up regular backups of your Supabase database

### 7. Testing in Production

After deployment, verify:

1. ✅ Website loads at `https://yourdomain.com`
2. ✅ Admin panel accessible at `https://yourdomain.com/admin`
3. ✅ Can create/edit products with images
4. ✅ Images upload to Supabase bucket and display correctly
5. ⚠️ Stripe payments: **disabled if STRIPE keys not configured**
6. ⚠️ Order processing: **manual/contact-based if payments disabled**
7. ⚠️ Email notifications: **disabled if EMAIL_BACKEND not configured**

If you enabled Stripe and/or email, test those features accordingly.

### 8. Troubleshooting

**Database connection fails:**
- Check if your server has IPv6 connectivity
- Verify `DATABASE_URL` is correct
- Ensure Supabase project is active and not paused

**Images not uploading:**
- Verify Supabase Storage bucket exists
- Check S3 credentials are correct
- Check bucket permissions (public/private)

**Static files not loading:**
- Ensure `collectstatic` ran successfully
- Check that `AWS_S3_CUSTOM_DOMAIN` is correct and accessible
- Verify bucket contains the static files

## Local vs Production `.env` Summary

**Local (`.env` for development):**
```bash
DATABASE_URL=sqlite:///db.sqlite3
DEBUG=True
# All other Supabase storage settings remain the same
```

**Production (`.env` for deployment):**
```bash
DATABASE_URL=postgresql://...@db.ityswbjguqeadyabvqrb.supabase.co:5432/postgres
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
# Live Stripe keys, email settings, etc.
```

Simply change `DATABASE_URL` and `DEBUG`, and add production-specific settings to switch from local to production.
