import environ
import os
import dj_database_url

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Set the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read .env file from BASE_DIR explicitly
env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_path):
    environ.Env.read_env(env_path)



# False if not in os.environ because of casting above
DEBUG = env('DEBUG')

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')



from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-k!n-x&*qlcx*&szyrhbn(ka=ipk93d7(rc6#rxkqd*vt(5%3&^'

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = ['*']
LOGOUT_REDIRECT_URL ='/'
LOGIN_REDIRECT_URL ='/'
LOGIN_URL = '/login/'

SESSION_COOKIE_AGE = 86400
CART_SESSION_ID = 'cart'



# Stripe Configuration (optional for production - will be disabled if not set)
STRIPE_API_KEY_PUBLISHABLE = env('STRIPE_API_KEY_PUBLISHABLE', default='')
STRIPE_API_KEY_HIDDEN = env('STRIPE_API_KEY_HIDDEN', default='')
STRIPE_SUCCESS_URL = env('STRIPE_SUCCESS_URL', default='/')
STRIPE_CANCEL_URL = env('STRIPE_CANCEL_URL', default='/')


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'theme',
    'django_browser_reload',
    "crispy_forms",
    "crispy_tailwind",
    'products',
    'cart',
    'ecommerce',
    'order',

    # amazon s3
    'storages',

]

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = [
    "127.0.0.1",
]

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'



DATABASE_URL = env('DATABASE_URL')


DATABASES = {
    "default":dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'
# TIME_ZONE = 'UTC'

USE_I18N = True


USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STATIC_ROOT = BASE_DIR /'static_root'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media/'




# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

APPEND_SLASH = False

JAZZMIN_SETTINGS ={
    'site_header': "Ecommerce",
    'site_brand': 'You order, we deliver',
    # 'site_logo': '/images/logo.jpg',
    'copyright': 'ecommerce.com',
}


# settings.py

# Email Configuration (optional for production - uses dummy backend if not configured)
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.dummy.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env('EMAIL_PORT', default=25)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='')
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=False)




AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL', default=None)
AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN', default=None)
AWS_QUERYSTRING_AUTH = env.bool('AWS_QUERYSTRING_AUTH', default=False)
AWS_S3_ADDRESSING_STYLE = "path"  # Use path-style addressing for Supabase

DEFAULT_FILE_STORAGE = env('DEFAULT_FILE_STORAGE')
STATICFILES_STORAGE = env('STATICFILES_STORAGE')
