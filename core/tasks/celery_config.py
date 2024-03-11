# Standard Library
import os

CELERY_REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
CELERY_REDIS_PORT = os.getenv("REDIS_PORT", 6379)
BROKER_URL = f"redis://{CELERY_REDIS_HOST}:{CELERY_REDIS_PORT}/0"  # Redis configuration
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_IMPORTS = ("core.tasks.tasks",)
