import imp
import redis
from utils.config import config

_redis_client = None


class RedisDb:
   def __init__(self):
      self.get_redis_client()

   @staticmethod
   def get_redis_client(new=False):
      global _redis_client

      try:
         if new or not _redis_client:
            _redis_client = redis.Redis(
                host=config['redis']['host'],
                port=config['redis']['port'],
                password=config['redis']['pass'],
                db=0)
      except Exception as ex:
         raise ex
      else:
         return _redis_client

   @staticmethod
   def get_data(key):
      try:
         redis_data = _redis_client.get(key)
      except Exception as ex:
         raise ex
      else:
         if redis_data is not None:
            return redis_data.decode('utf-8')
         else:
            return None

   @staticmethod
   def set_data(key, data, time):
      try:
         _redis_client.set(key, str(data).encode('utf-8'), time)
      except Exception as ex:
         raise ex
      else:
         pass

   @staticmethod
   def delete_data(key):
      try:
         _redis_client.delete(key)
      except Exception as ex:
         raise ex
      else:
         pass
