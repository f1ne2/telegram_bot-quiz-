from __future__ import annotations
from flask import Flask, request
from dotenv import load_dotenv
import os
from os.path import join, dirname
from bot.db import WorkWithDB
from bot.interface import FormalInterface
import requests
import json

app = Flask(__name__)
db: FormalInterface = WorkWithDB()


def send_message(chat_id: str, text: str) -> None:
    method: str = "sendMessage"
    token: str = get_from_env("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


def get_from_env(key: str) -> str:
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)
    return os.environ.get(key)


def get_answers() -> json:
    with open('assets/questions.json', 'r', encoding='utf-8') as f:
        question: json = json.load(f)
    return question


def get_result(chat_id: str) -> int:
    correct_answers: int = 0
    answer_arr: [] = db.range(f'{chat_id}')
    answer_arr = [line.decode("utf-8").rstrip().lower() for line in answer_arr]
    answer_arr = answer_arr[::-1]
    question: json = get_answers()
    for i in range(len(answer_arr)):
        if answer_arr[i] == question["questions"][i]["answer"]:
            correct_answers += 1
    return correct_answers


@app.route("/", methods=["GET", "POST"])
def receive_update() -> json:
    if request.method == "POST":
        msg = request.get_json()
        chat_id = msg["message"]["chat"]["id"]
        question = get_answers()

        if request.json["message"]["text"] == "/start":
            if db.exist(f'{chat_id}'):
                db.delete(f'{chat_id}')
            send_message(chat_id, "Welcome to the quiz!!! \n You have to answer the 5 questions for 5 minutes \n "
                                  "Let's go!  ")
            db.push(f'{chat_id}', 'answers')
            send_message(chat_id, question["questions"][0]["question"])
        elif db.exist(f'{chat_id}'):
            db.push(f'{chat_id}', request.json["message"]["text"])
            if db.len(f'{chat_id}')-1 == len(question["questions"]):
                result: int = get_result(chat_id)
                send_message(chat_id, f"{result}/{db.len(f'{chat_id}')-1} "
                                      f"correct answers. \n Enter /start if you would try again")
                db.delete(f'{chat_id}')
            else:
                send_message(chat_id, question["questions"][db.len(f'{chat_id}')-1]["question"])

    return {"ok": True}


if __name__ == "__main__":
    app.run()
