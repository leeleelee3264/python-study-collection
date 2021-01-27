# 외부 api 접속용

# db info, default tpi outer
name = 'dev_db'
userId = 'root'
userPw = '1234'
host = 'db-in-test-linux-server'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': name,
        'USER': userId,
        'PASSWORD': userPw,
        'HOST': host,
        'PORT': '3306',
        'OPTIONS': {

        }
    },
}
