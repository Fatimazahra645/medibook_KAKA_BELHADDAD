from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-medibook-change-in-production")


DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    'jazzmin','django.contrib.admin','django.contrib.auth',
    'django.contrib.contenttypes','django.contrib.sessions',
    'django.contrib.messages','django.contrib.staticfiles',
    'accounts','doctors','appointments','ai_orientation',
    'patients','dashboard','notifications',
]




AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = '/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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



TEMPLATES = [{'BACKEND':'django.template.backends.django.DjangoTemplates',
    'DIRS':[BASE_DIR/"templates"],'APP_DIRS':True,
    'OPTIONS':{'context_processors':[
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]


DATABASES = {"default":{"ENGINE":"django.db.backends.postgresql",
    "NAME":os.getenv("DB_NAME","medibook_db"),"USER":os.getenv("DB_USER","medibook_user"),
    "PASSWORD":os.getenv("DB_PASSWORD","medibook_password"),
    "HOST":os.getenv("DB_HOST","localhost"),"PORT":os.getenv("DB_PORT","5432"),}}



AUTH_PASSWORD_VALIDATORS = [
    {"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"},
]



LANGUAGE_CODE='fr-fr'; TIME_ZONE='Africa/Algiers'; USE_I18N=True; USE_TZ=True


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL="/media/"
MEDIA_ROOT=BASE_DIR/"media"


_sd=BASE_DIR/"static"; STATICFILES_DIRS=[_sd] if _sd.exists() else []


STATICFILES_STORAGE=("django.contrib.staticfiles.storage.StaticFilesStorage" if DEBUG
    else "whitenoise.storage.CompressedManifestStaticFilesStorage")
EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"
JAZZMIN_SETTINGS={"site_title":"MediBook Admin","site_header":"MediBook",
    "site_brand":"MediBook","welcome_sign":"Administration MediBook","copyright":"MediBook 2025"}
