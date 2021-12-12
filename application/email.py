import os

from celery.utils.serialization import strtobool

BITHR_LOGO_PNG = os.environ.get("APPS_BITHR_LOGO_PNG")
FACEBOOK_URL = os.environ.get("APPS_FACEBOOK_URL")
FACEBOOK_PNG = os.environ.get("APPS_FACEBOOK_PNG")
TWITTER_URL = os.environ.get("APPS_TWITTER_URL")
TWITTER_PNG = os.environ.get("APPS_TWITTER_PNG")
TELEGRAM_URL = os.environ.get("APPS_TELEGRAM_URL")
TELEGRAM_PNG = os.environ.get("APPS_TELEGRAM_PNG")
YOUTUBE_URL = os.environ.get("APPS_YOUTUBE_URL")
YOUTUBE_PNG = os.environ.get("APPS_YOUTUBE_PNG")
GOOGLE_PLAY_PNG = os.environ.get("APPS_GOOGLE_PLAY_PNG")
APPLE_STORE_PNG = os.environ.get("APPS_APPLE_STORE_PNG")
EMAIL_NOTIFICATION_SENDER = os.environ.get("APP_EMAIL_NOTIFICATION_SENDER")
EMAIL_HOST = os.environ.get("APPS_EMAIL_HOST")
EMAIL_PORT = os.environ.get("APPS_EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("APPS_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("APPS_EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = strtobool(os.environ.get("APPS_EMAIL_USE_TLS"))

EMAIL_BACKEND = os.environ.get("APPS_EMAIL_BACKEND")