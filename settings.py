import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = (
    'app', 
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'northwind2',
        'USER': 'dbadmin',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
# CHANGE THE SECRET KEY IN YOUR CODE
SECRET_KEY = '4cCI6MTYzOTQ0NzgwNiwiaWF0IjoxNjM5NDQ3ODA2fQ' 