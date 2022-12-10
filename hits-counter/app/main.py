from fastapi import FastAPI
from redis_om import get_redis_connection

redis = get_redis_connection(
    host="redis",
    port=6379
)

app = FastAPI()

@app.post("/hits")
async def hits():
    """ Increments the hit counter and return the current value.
    """
    hits = redis.incr("hits")
    return {"hits": hits}

@app.get("/hits/health")
async def health_check():
    """ Access redis and returns the current value of the hit counter
    """
    redis.setnx("hits", 0)
    hits = redis.get("hits")
    return {"hits": hits}
