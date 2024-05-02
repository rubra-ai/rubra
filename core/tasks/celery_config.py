# Standard Library
from core.common import get_redis_url

BROKER_URL = get_redis_url()
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_IMPORTS = ("core.tasks.tasks",)
