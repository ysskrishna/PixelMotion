from redis import Redis
from rq import Queue
from pm_common.core.config import BaseConfig

class RedisConnection:
    _instance = None
    _redis_conn = None
    _jobs_queue_conn = None
    _jobs_queue = None
    _config = BaseConfig()

    @classmethod
    def initialize(cls):
        if cls._instance is None:
            cls._instance = cls()
            
            cls._config.validate_redis_config()

            cls._redis_conn = Redis(
                host=cls._config.REDIS_HOST, 
                port=cls._config.REDIS_PORT, 
                db=1
            )
            cls._jobs_queue_conn = Redis(
                host=cls._config.REDIS_HOST, 
                port=cls._config.REDIS_PORT, 
                db=0
            )
            cls._jobs_queue = Queue(connection=cls._jobs_queue_conn)
        return cls._instance

    @classmethod
    def get_redis_connection(cls) -> Redis:
        if cls._redis_conn is None:
            cls.initialize()
        return cls._redis_conn

    @classmethod
    def get_jobs_queue_conn(cls) -> Redis:
        if cls._jobs_queue_conn is None:
            cls.initialize()
        return cls._jobs_queue_conn

    @classmethod
    def get_jobs_queue(cls) -> Queue:
        if cls._jobs_queue is None:
            cls.initialize()
        return cls._jobs_queue