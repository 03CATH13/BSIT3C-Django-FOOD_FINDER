from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-zsnno#^l!whuzs%55j6*366px#r09+borh$1^2mj*_ovz47!o_'
DEBUG = True

ALLOWED_HOSTS = ['*'] 

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.food_finder',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'mysite.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

JAZZMIN_SETTINGS = {
    "site_title": "Kabankalan Eats Admin",
    "site_header": "Kabankalan Eats",
    "site_brand": "Kabankalan Eats",
    "site_logo": None,
    "site_logo_classes": "img-circle",
    "welcome_sign": "Welcome sa Kabankalan Eats Admin",
    "copyright": "Kabankalan Eats - BSIT3C - 2026",
    "search_model": ["food_finder.Restaurant"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "/", "new_window": False, "icon": "fas fa-home"},
        {"name": "View Site", "url": "/", "new_window": False, "icon": "fas fa-eye"},
        {"name": "Restaurants", "url": "admin:food_finder_restaurant_changelist", "icon": "fas fa-utensils"},
        {"name": "Menu", "url": "admin:food_finder_menuitem_changelist", "icon": "fas fa-book-open"},
    ],
    "usermenu_links": [
        {"name": "Balik sa Home", "url": "/", "new_window": False, "icon": "fas fa-home"},
        {"model": "auth.user"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["food_finder", "auth"],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "food_finder": "fas fa-utensils",
        "food_finder.Restaurant": "fas fa-store",
        "food_finder.MenuItem": "fas fa-bowl-rice",
        "food_finder.Review": "fas fa-star",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    # === GIN-ADD KO DIRI ANG FIX PARA INDI NA MAG-BLANGKO ===
    # Daan: related_modal_active True + custom_admin.css = nagapa-blangko sa Menu page
    "related_modal_active": False,
    # GIN-KUHA ANG custom_admin.css - amo ni ang nagpa-puti sang page
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "default_theme_mode": "light",
    "navbar": "navbar-dark",
    "navbar_fixed": True,
    "navbar_small_text": False,
    "navbar_border": True,
    "sidebar": "sidebar-dark-pink",
    "sidebar_fixed": True,
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "brand_colour": "navbar-pink",
    "accent": "accent-pink",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
    "actions_sticky_top": True,
}

if sys.version_info >= (3, 14):
    from django.template.context import BaseContext
    from copy import copy
    
    def _patched_copy(self):
        duplicate = BaseContext()
        duplicate.__class__ = self.__class__
        duplicate.__dict__ = copy(self.__dict__)
        duplicate.dicts = self.dicts[:]
        return duplicate
    
    BaseContext.__copy__ = _patched_copy