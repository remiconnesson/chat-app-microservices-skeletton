from fastapi import FastAPI
from redis_om import get_redis_connection

redis = get_redis_connection(
    host="redis",
    port=6379
)

app = FastAPI()

@app.post("/")
async def root():
    hits = redis.incr("hits")
    return {"hits": hits}

@app.get("/ping")
async def health_check():
    redis.setnx("hits", 0)
    hits = redis.get("hits")
    return {"hits": hits}
