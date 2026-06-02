from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-default-key")

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*"]


# =====================
# APPS
# =====================
INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # apps projet
    'accounts',
    'doctors',
    'appointments',
    'ai_orientation',
    'patients',
    'dashboard',
    'notifications',
]

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/login/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =====================
# TEMPLATES
# =====================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# =====================
# MIDDLEWARE (IMPORTANT FIX STATIC)
# =====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # FIX STATIC CSS/JS
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'medibook_project.urls'
WSGI_APPLICATION = 'medibook_project.wsgi.application'


# =====================
# DATABASE
# =====================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "medibook_db"),
        "USER": os.getenv("DB_USER", "medibook_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", "medibook_password"),
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}


# =====================
# PASSWORD VALIDATION
# =====================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# =====================
# INTERNATIONALIZATION
# =====================
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Casablanca'
USE_I18N = True
USE_TZ = True


# =====================
# STATIC FILES (IMPORTANT FIX)
# =====================
STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
] if (BASE_DIR / "static").exists() else []

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# WhiteNoise (IMPORTANT)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# =====================
# JAZZMIN CONFIG
# =====================
JAZZMIN_SETTINGS = {
    "site_title": "MediBook Admin",
    "site_header": "MediBook",
    "site_brand": "MediBook Health",
    "welcome_sign": "Bienvenue sur MediBook",
    "copyright": "MediBook © 2026",

    "theme": "cosmo",

    "icons": {
        "auth": "fas fa-users-cog",
        "accounts": "fas fa-user",
        "patients": "fas fa-user-injured",
        "doctors": "fas fa-user-md",
        "appointments": "fas fa-calendar-check",
        "notifications": "fas fa-bell",
    },

    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index"},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-teal",
    "navbar": "navbar-primary navbar-dark",
    "sidebar": "sidebar-dark-primary",
}