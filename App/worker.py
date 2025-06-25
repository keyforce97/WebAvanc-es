from App.redis_client import redis_client
from rq.connection import Connection # type: ignore
from rq import Connection
from rq import Worker


if __name__ == "__main__":
    with Connection(redis_client):
        worker = Worker(['default'])
        worker.work()

