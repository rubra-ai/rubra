import os

CELERY_REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
BROKER_URL = f'redis://{CELERY_REDIS_HOST}:6379/0'  # Redis configuration
CELERY_RESULT_BACKEND = f'redis://{CELERY_REDIS_HOST}:6379/0'
CELERY_IMPORTS = ("app.tasks", )
