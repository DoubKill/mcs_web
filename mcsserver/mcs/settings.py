"""
Django settings for mcs project.

Generated by 'django-admin startproject' using Django 2.1.15.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import datetime
import json
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'km6wln_e0mjw*uc)o^2%yfc^%kasbj&l)$s3(cy9a8kkxyplwq'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = eval(os.environ.get('DEBUG', 'True'))
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'django_filters',
    'agv.apps.AgvConfig',
    'user.apps.UserConfig',
    'basics.apps.BasicsConfig',
    'monitor.apps.MonitorConfig',
    'openapi.apps.OpenapiConfig'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mcs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'fronted')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mcs.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


try:
    with open('mcs/db_conf.json', 'r', encoding='utf-8') as f:
        jsonFile = json.load(f)
        dbConfig = jsonFile.get('db_conf')
except Exception as e:
    dbConfig = {}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # 数据库引擎
        'HOST': dbConfig.get('host'),  # HOST
        'NAME': dbConfig.get('database'),  # 数据库名称
        'USER': dbConfig.get('user'),  # 用户名
        'PASSWORD': dbConfig.get('password'),  # 密码
        'PORT': dbConfig.get('port'),  # 端口
    }
}

try:
    from .local_settings import *
except ImportError:
    pass

# drf通用配置
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',  # 文档
    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),  # 权限
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ) if DEBUG else ('rest_framework_jwt.authentication.JSONWebTokenAuthentication',),  # 认证
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),  # 过滤
    'DEFAULT_PAGINATION_CLASS': 'mcs.paginations.DefaultPageNumberPagination',  # 分页
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer', ),
}


LOGGING_DIR = os.environ.get('LOGGING_DIR', os.path.join(BASE_DIR, 'logs'))
if not os.path.exists(LOGGING_DIR):
    os.mkdir(LOGGING_DIR)

# 日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] '
                      '[%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'
        },
        'django_request': {
            'format': '%(levelname)s %(asctime)s %(pathname)s %(module)s %(lineno)d %(message)s'
                      ' status_code:%(status_code)d',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'django_db_backends': {
            'format': '%(levelname)s %(asctime)s %(pathname)s %(module)s %(lineno)d %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'django_db_backends': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'django_db_backends'
        },
        'django_request': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'django_request'
        },
        'timedRotatingFile': {
            'level': 'DEBUG',
            'class': 'mcs.custom_log.CommonTimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'api_log.log'),
            'when': 'midnight',
            'backupCount': 10,
            'formatter': 'standard',
            'interval': 1,
        },
        'errorFile': {
            'level': 'DEBUG',
            'class': 'mcs.custom_log.CommonTimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'error.log'),
            'when': 'midnight',
            'backupCount': 10,
            'formatter': 'standard',
            'interval': 1,
        },
        'sendFile': {
            'level': 'DEBUG',
            'class': 'mcs.custom_log.CommonTimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'send.log'),
            'when': 'midnight',
            'backupCount': 10,
            'formatter': 'standard',
            'interval': 1,
        },
        'dispatchFile': {
            'level': 'DEBUG',
            'class': 'mcs.custom_log.CommonTimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'dispatch.log'),
            'when': 'midnight',
            'backupCount': 10,
            'formatter': 'standard',
            'interval': 1,
        },
        'apschedulerFile': {
            'level': 'DEBUG',
            'class': 'mcs.custom_log.CommonTimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'apscheduler.log'),
            'when': 'midnight',
            'backupCount': 10,
            'formatter': 'standard',
            'interval': 1,
        },
        'collectFile': {
            'level': 'DEBUG',
            'class': 'mcs.custom_log.CommonTimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'collect.log'),
            'when': 'midnight',
            'backupCount': 10,
            'formatter': 'standard',
            'interval': 1,
        },
        'routeFile': {
            'level': 'DEBUG',
            'class': 'mcs.custom_log.CommonTimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'route.log'),
            'when': 'midnight',
            'backupCount': 10,
            'formatter': 'standard',
            'interval': 1,
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['django_db_backends'],
            'propagate': True,
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'django.request': {
            'handlers': ['django_request'],
            'level': 'ERROR',
            'propagate': False,
        },
        'api_log': {  # API日志
            'handlers': ['timedRotatingFile'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'error_log': {  # API错误日志
            'handlers': ['errorFile'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'send_log': {  # 任务发送
            'handlers': ['sendFile'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'dispatch_log': {  # 调度
            'handlers': ['dispatchFile'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'apscheduler_log': {  # 定时任务
            'handlers': ['apschedulerFile'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'collect_log': {  # 数据采集
            'handlers': ['collectFile'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'route_log': {  # 数据采集
            'handlers': ['routeFile'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/


LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'fronted/static')

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = '/media/'
if not os.path.exists(MEDIA_ROOT):
    os.mkdir(MEDIA_ROOT)

# 跨域允许的请求方式，可以使用默认值，默认的请求方式为:
# from corsheaders.defaults import default_methods
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

# 允许跨域的请求头，可以使用默认值，默认的请求头为:
# from corsheaders.defaults import default_headers
# CORS_ALLOW_HEADERS = default_headers

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

# 跨域请求时，是否运行携带cookie，默认为False
CORS_ALLOW_CREDENTIALS = True
# 允许所有主机执行跨站点请求，默认为False
# 如果没设置该参数，则必须设置白名单，运行部分白名单的主机才能执行跨站点请求
CORS_ORIGIN_ALLOW_ALL = True

AUTH_USER_MODEL = 'user.User'

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=365),
    'JWT_ALLOW_REFRESH': True,
}

COMMON_READ_ONLY_FIELDS = ('created_time', 'last_updated_time', 'delete_time',
                           'delete_flag', 'created_user', 'last_updated_user',
                           'delete_user')

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
