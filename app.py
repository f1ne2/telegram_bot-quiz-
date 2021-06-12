from __future__ import annotations
from flask import Flask, request
from dotenv import load_dotenv
import os
from os.path import join, dirname
import requests
import json
import redis

app = Flask(__name__)
redisClient = redis.Redis(host='127.0.0.1', port=6379, db=0)


def send_message(chat_id, text) -> None:
    method = "sendMessage"
    token = get_from_env("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


def get_from_env(key):
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)
    return os.environ.get(key)


def get_answers():
    with open('questions.json', 'r', encoding='utf-8') as f:
        question = json.load(f)
    return question


def get_result(chat_id):
    correct_answers = 0
    answer_arr = redisClient.lrange(f'{chat_id}', 0, redisClient.llen(f'{chat_id}')-2)
    answer_arr = [line.decode("utf-8").rstrip().lower() for line in answer_arr]
    answer_arr = answer_arr[::-1]
    question = get_answers()
    for i in range(len(answer_arr)):
        if answer_arr[i] == question["questions"][i]["answer"]:
            correct_answers += 1
    return correct_answers


@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        msg = request.get_json()
        chat_id = msg["message"]["chat"]["id"]
        question = get_answers()

        if request.json["message"]["text"] == "/start":
            if redisClient.exists(f'{chat_id}'):
                redisClient.delete(f'{chat_id}')
            send_message(chat_id, "Welcome to the quiz!!! \n You have to answer the 5 questions for 5 minutes \n "
                                  "Let's go!  ")
            redisClient.lpush(f'{chat_id}', 'answers')
            send_message(chat_id, question["questions"][0]["question"])
        elif redisClient.exists(f'{chat_id}'):
            redisClient.lpush(f'{chat_id}', request.json["message"]["text"])
            if redisClient.llen(f'{chat_id}')-1 == len(question["questions"]):
                result = get_result(chat_id)
                send_message(chat_id, f"{result}/{redisClient.llen(f'{chat_id}')-1} "
                                      f"correct answers. \n Enter /start if you would try again")
                redisClient.delete(f'{chat_id}')
            else:
                send_message(chat_id, question["questions"][redisClient.llen(f'{chat_id}')-1]["question"])

    return {"ok": True}


if __name__ == "__main__":
    app.run()
