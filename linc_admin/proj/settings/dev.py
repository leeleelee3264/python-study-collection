from proj.settings.base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'swatch',
        'USER': 'linc',
        'PASSWORD': 'linc',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
        },
    },
}

DATABASES['ncs'] = DATABASES['default'].copy()
DATABASES['ncs']['NAME'] = 'ncs'

DATABASES['qliq'] = DATABASES['default'].copy()
DATABASES['qliq']['NAME'] = 'qliq'


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

RUNNING_MODE = 'DEV'
