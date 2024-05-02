import os

_mongo_url = ""
_redis_url = ""
_litellm_url = ""


def get_mongo_url():
    global _mongo_url
    if _mongo_url:
        return _mongo_url

    _mongo_url = os.getenv("MONGODB_URL")
    if _mongo_url:
        return _mongo_url

    host = os.getenv("MONGODB_HOST", "localhost")
    user = os.getenv("MONGODB_USER")
    password = os.getenv("MONGODB_PASSWORD")
    port = os.getenv("MONGODB_PORT", 27017)
    if (
        not user or not password
    ):  # if any of these not passed, just return unauthenticated url
        _mongo_url = f"mongodb://{host}:{port}"
        return _mongo_url

    _mongo_url = f"mongodb://{user}:{password}@{host}:{port}"
    return _mongo_url


def get_litellm_proxy_url():
    global _litellm_url
    if _litellm_url:
        return _litellm_url

    host = os.getenv("LITELLM_HOST", "localhost")
    port = os.getenv("LITELLM_PORT", 8002)

    _litellm_url = f"http://{host}:{port}"
    return _litellm_url


def get_redis_url():
    global _redis_url
    if _redis_url:
        return _redis_url

    _redis_url = os.getenv("REDIS_URL")
    if _redis_url:
        return _redis_url

    host = os.getenv("REDIS_HOST", "localhost")
    user = os.getenv("REDIS_USER")
    password = os.getenv("REDIS_PASSWORD")
    port = os.getenv("REDIS_PORT", 6379)

    if not password:
        _redis_url = f"redis://{host}:{port}/0"
        return _redis_url

    _redis_url = f"redis://{user}:{password}@{host}:{port}/0"
    return _redis_url
