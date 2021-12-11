from proj.settings.base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'swatch',
        'USER': 'dnx',
        'PASSWORD': 'dnx1221#$',
        'HOST': '211.115.110.13',
        'PORT': '3306',
        'OPTIONS': {
        },
    },
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://13.124.180.163:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

RUNNING_MODE = 'PROD'



### APPLICATION SETTING ###
SW_REST_URL = 'http://api.dnx.kr'
