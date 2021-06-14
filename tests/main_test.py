import unittest
from main import *


class TestMain(unittest.TestCase):
    def test_get_answer(self):
        res = get_answers()
        self.assertEqual(res, {"questions": [{"question": "How many days in the year?", "answer": "365"},
                                             {"question": "How many hours in the year?", "answer": "8760"},
                                             {"question": "What planetary system we live in?", "answer": "solar"},
                                             {"question": "In what country were last summer Olympic games?",
                                              "answer": "brazil"},
                                             {"question": "In what country were last winter Olympic games?",
                                              "answer": "south korea"}]})

    def test_get_result(self):
        res = get_result(776685908)
        self.assertEqual(res, 0)
