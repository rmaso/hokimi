import os
gettext = lambda s: s
DATA_DIR = os.path.dirname(os.path.dirname(__file__))
"""
Django settings for hokimicms project.

Generated by 'django-admin startproject' using Django 1.8.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    # safe value used for development when DJANGO_SECRET_KEY might not be set
    '(n)gz(a2gf$x(8#3w63ustb(pv@ga4@gk#_z@fzw!$$f%ynk4x'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition





ROOT_URLCONF = 'hokimicms.urls'



WSGI_APPLICATION = 'hokimicms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# from . import database

# DATABASES = {
#     'default': database.config()
# }

import dj_database_url
DATABASES = {
    'default': dj_database_url.config()
}



# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')

from machina import MACHINA_MAIN_STATIC_DIR

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'hokimicms', 'static'),
    MACHINA_MAIN_STATIC_DIR,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SITE_ID = 1

from machina import MACHINA_MAIN_TEMPLATE_DIR

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'hokimicms', 'templates'),
            MACHINA_MAIN_TEMPLATE_DIR,
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'cms.context_processors.cms_settings',
                'aldryn_boilerplates.context_processors.boilerplate',
                'aldryn_snake.template_api.template_processor',
                'machina.core.context_processors.metadata',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'aldryn_boilerplates.template_loaders.AppDirectoriesLoader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader'
            ],
        },
    },
]


MIDDLEWARE_CLASSES = (
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'machina.apps.forum_permission.middleware.ForumPermissionMiddleware',
)

from machina import get_apps as get_machina_apps

INSTALLED_APPS = [
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'djangocms_column',
    'djangocms_link',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_filer_utils',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_googlemap',
    'djangocms_video',
    'aldryn_bootstrap3',
    'absolute',
    'aldryn_forms',
    'aldryn_forms.contrib.email_notifications',
    # 'aldryn_google_analytics',
    'captcha',
    'emailit',
    'hokimicms',
    # 'competition',
    'crispy_forms',
    'test',
    'my_custom_social_addon',
    'torneos',
    # Machina related apps:
    'mptt',
    'haystack',
    'widget_tweaks',
] + get_machina_apps()

LANGUAGES = (
    ## Customize this
    ('es', gettext('Castellano')),
    ('en', gettext('English')),
)

CMS_LANGUAGES = {
    ## Customize this
    1: [
        {
            'code': 'es',
            'name': gettext('Castellano'),
            'fallbacks': ['en'],
            'public': True,
        },
        {
            'code': 'en',
            'name': gettext('English'),
            'redirect_on_fallback': True,
            'public': True,
        },
    ],
    'default': {
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    },
}

CMS_TEMPLATES = (
    ## Customize this
    ('fullwidth.html', 'Fullwidth'),
    ('sidebar_left.html', 'Sidebar Left'),
    ('sidebar_right.html', 'Sidebar Right'),
    ('tpl_home.html', 'Home template'),
    ('torneo.html', 'Torneos'),
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

DJANGOCMS_STYLE_CHOICES = ['container', 'content', 'teaser', 'feature-visual', 'feature-content', 'text-center', 'section-cyan', 'section-gray']

ALDRYN_BOILERPLATE_NAME='bootstrap3'

GOOGLE_ANALYTICS_ID='UA-94087556-1'
GOOGLE_ANALYTICS_USE_UNIVERSAL=False
GOOGLE_ANALYTICS_TRACK_INDIVIDUALS=False

# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIGRATION_MODULES = {
    
}

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

HAYSTACK_CONNECTIONS = {
  'default': {
    'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
  },
}

CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
  },
  'machina_attachments': {
    'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    'LOCATION': '/tmp',
  }
}

MACHINA_DEFAULT_AUTHENTICATED_USER_FORUM_PERMISSIONS = [
    'can_see_forum',
    'can_read_forum',
    'can_start_new_topics',
    'can_reply_to_topics',
    'can_edit_own_posts',
    'can_post_without_approval',
    'can_create_polls',
    'can_vote_in_polls',
    'can_download_file',
]


