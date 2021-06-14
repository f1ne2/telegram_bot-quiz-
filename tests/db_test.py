import unittest
from main import *
import redis


class TestMain(unittest.TestCase):
    def setUp(self):
        self.redisClient = redis.Redis(host='127.0.0.1', port=6379, db=0)
        self.db: FormalInterface = WorkWithDB()

    def test_push(self):
        chat_id = '776685908'
        value = 'Hello'
        self.db.push(chat_id, value)
        self.assertEqual(self.redisClient.exists(chat_id), True)

    def test_delete(self):
        chat_id = '776685909'
        value = 'Hello'
        self.db.push(chat_id, value)
        self.db.delete(chat_id)
        self.assertEqual(self.redisClient.exists(chat_id), False)

    def test_exist(self):
        chat_id = '776685909'
        value = 'Hello'
        self.db.push(chat_id, value)
        self.assertEqual(db.exist(chat_id), True)

    def test_len(self):
        chat_id = '776685910'
        value = 'Next'
        self.db.push(chat_id, value)
        value2 = 'Next2'
        self.db.push(chat_id, value2)
        self.assertEqual(db.len(chat_id), 2)

    def test_range(self):
        chat_id = '776685912'
        value = 'Next'
        self.db.push(chat_id, value)
        value2 = 'Next2'
        self.db.push(chat_id, value2)
        value3 = 'Next3'
        self.db.push(chat_id, value3)
        self.assertEqual(db.range(chat_id), [b'Next3', b'Next2'])



