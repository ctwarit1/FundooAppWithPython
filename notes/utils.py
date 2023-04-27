import json

import redis


class RedisManager:

    def __init__(self):
        self.redis = redis.Redis(host="localhost", port=6379, db=0)

    def save(self, user_id, notes):
        user_id = str(user_id)
        note_id = str(notes.get("id"))
        self.redis.hset(user_id, note_id, json.dumps(notes))

    def get(self, user_id):
        user_id = str(user_id)
        print(user_id)
        redis_notes = self.redis.hgetall(user_id)
        if redis_notes:
            data = [json.loads(x) for x in redis_notes.values()]
            return data
        return {}

    def delete(self, user_id, note_id):
        user_id = str(user_id)
        note_id = str(note_id)
        redis_notes = self.redis.hget(user_id, note_id)
        if redis_notes:
            self.redis.hdel(user_id, note_id)
