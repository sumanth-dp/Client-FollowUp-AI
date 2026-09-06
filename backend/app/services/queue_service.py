import json

from backend.app.core.redis import redis_client

QUEUE_NAME = "follow_up_queue"

def enqueue_follow_up(follow_up_id: int):
    job = {
    "follow_up_id": follow_up_id
    }

    
    redis_client.lpush(
        QUEUE_NAME,
        json.dumps(job),
    )
    
