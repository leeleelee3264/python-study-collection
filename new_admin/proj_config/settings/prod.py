# 내부 tpi 접속용

# db info, default tpi outer
name = 'prod_db'
userId = 'root'
userPw = '1234'
host = 'db-in-linux-server'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': name,
        'USER': userId,
        'PASSWORD': userPw,
        'HOST': host,
        'PORT': 3306,
        'OPTIONS' : {

        }
    }
}
