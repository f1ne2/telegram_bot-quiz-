from bot.interface import FormalInterface
import redis


class WorkWithDB(FormalInterface):
    def __init__(self):
        self.redisClient = redis.Redis(host='127.0.0.1', port=6379, db=0)

    def push(self, chat_id: str, value: str):
        return self.redisClient.lpush(f'{chat_id}', value)

    def delete(self, chat_id: str):
        return self.redisClient.delete(f'{chat_id}')

    def exist(self, chat_id: str):
        return self.redisClient.exists(f'{chat_id}')

    def len(self, chat_id: str):
        return self.redisClient.llen(f'{chat_id}')

    def range(self, chat_id: str):
        answer_arr = self.redisClient.lrange(f'{chat_id}', 0, self.redisClient.llen(f'{chat_id}')-2)
        answer_arr = [line.decode("utf-8").rstrip().lower() for line in answer_arr]
        return answer_arr[::-1]
