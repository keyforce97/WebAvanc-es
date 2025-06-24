from rq import Worker
from rq.connections import Connection
from App.redis_client import redis_client

if __name__ == "__main__":
    with Connection(redis_client):
        worker = Worker(['default'])
        worker.work()
