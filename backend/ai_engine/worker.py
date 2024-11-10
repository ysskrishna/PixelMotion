from src.core.config import config
from rq import Worker, Queue, Connection
from pm_common.core.redis_utils import RedisConnection

jobs_queue_conn = RedisConnection.get_jobs_queue_conn()
listen = ['default']

if __name__ == '__main__':
    with Connection(jobs_queue_conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()