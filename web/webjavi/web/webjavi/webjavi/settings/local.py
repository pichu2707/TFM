from .base import *



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',#postgresql_psycopg2 sqlite3
        'NAME': 'dbwebjavi',
        'USER': 'javilazaro',
        'PASSWORD': 'JaviLazaro',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR.child('static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')

#ckeditor settings
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/3.7.0/jquery.min.js"'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['TextColor','Format','FontSize', 'Link'],
            ['Smiley', 'Image','Iframe'],
            ['RemoveFormat', 'Source']
        ],
        'stylesSet':[

        ],
    }
}