
import redis
import json
import config

def connect_to_redis():
    return redis.Redis(config.REDIS_HOST, config.REDIS_PORT)

cache = connect_to_redis()

def load_from_cache(key):
    results = cache.get(key)
    if results is not None :
        return json.loads(results)
    return None

def add_to_cache(key, results):
    results = json.dumps(results)
    cache.delete(key)
    cache.set(key, results)
    cache.expire(key, config.CACHE_TTL)
