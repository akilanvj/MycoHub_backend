from rq import Worker, Queue, Connection
from redis import Redis
from main import process_file, redis_conn

if __name__ == '__main__':
    with Connection(Redis()):
        worker = Worker(Queue(), connection=Redis())
        worker.work()
