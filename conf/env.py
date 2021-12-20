
# ================================================= #
# ************** mysql  *************************** #
# ================================================= #
# MYSQL/SQLITE3
DATABASE_TYPE = "MYSQL"
DATABASE_HOST = "127.0.0.1"
DATABASE_PORT = 5432
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "123456a@"
DATABASE_NAME = "django-vue-admin"

# ================================================= #
# ************** redis  *************************** #
# ================================================= #
REDIS_ENABLE = True
REDIS_DB = 1
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = ''
# celery 定时任务redis 库号
CELERY_DB = 2

# ================================================= #
# ************** 默认配置  ************** #
# ================================================= #
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False
CAPTCHA_STATE = True
API_LOG_ENABLE = True
API_LOG_METHODS = ['POST', 'DELETE', 'PUT'] # 'ALL' or ['POST', 'DELETE']
INTERFACE_PERMISSION = True
ENABLE_LOGIN_LOCATION = True
