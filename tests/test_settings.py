""" Tests Settings
"""

SECRET_KEY = "fake-key"

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    # Extra apps
    "django_celery_beat",
    # Local apps
    "core_main_app",
    "core_dashboard_common_app",
    "core_dashboard_app",
    "core_parser_app",
    "core_curate_app",
    "core_explore_common_app",
    "tests",
]

# IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

MIDDLEWARE = (
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core_main_app.utils.custom_context_processors.domain_context_processor",
                "django.template.context_processors.i18n",
            ],
        },
    },
]

CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CUSTOM_NAME = "Curator"

MONGODB_INDEXING = False
MONGODB_ASYNC_SAVE = False
ROOT_URLCONF = "tests.urls"
ENABLE_SAML2_SSO_AUTH = False
RECORD_PER_PAGE_PAGINATION = 10
