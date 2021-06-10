from __future__ import annotations
from flask import Flask, request
from dotenv import load_dotenv
import os
from os.path import join, dirname
import requests
import json

app = Flask(__name__)


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


def get_result(chat_id):
    answer_arr = []
    correct_answers = 0
    with open(f'{chat_id}.txt', 'r', encoding='utf-8') as f:
        for line in f:
            answer_arr.append(line)
    answer_arr = [line.rstrip() for line in answer_arr]
    answer_arr = [line.lower() for line in answer_arr]
    with open('questions.json', 'r', encoding='utf-8') as f:
        question = json.load(f)
    for i in range(len(answer_arr)):
        if answer_arr[i] == question["questions"][i]["answer"]:
            correct_answers += 1
    return correct_answers


@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        msg = request.get_json()
        chat_id = msg["message"]["chat"]["id"]
        if request.json["message"]["text"] == "/start":
            if os.path.exists(f'{chat_id}.txt'):
                os.remove(f'{chat_id}.txt')
            send_message(chat_id, "Welcome to the quiz!!! Enter /quiz to quiz start")
        elif request.json["message"]["text"] == "/quiz":
            with open('questions.json', 'r', encoding='utf-8') as f:
                question = json.load(f)
            with open(f'{chat_id}.txt', 'w', encoding='utf-8') as f:
                pass
            send_message(chat_id, question["questions"][0]["question"])
        else:
            if os.path.exists(f'{chat_id}.txt'):
                with open(f'{chat_id}.txt', 'a', encoding='utf-8') as file:
                    file.write(msg["message"]["text"] + '\n')
                answer_arr = []
                with open(f'{chat_id}.txt', 'r', encoding='utf-8') as f:
                    for line in f:
                        answer_arr.append(line)
                with open('questions.json', 'r', encoding='utf-8') as f:
                    question = json.load(f)
                if len(answer_arr) == len(question["questions"]):
                    result = get_result(chat_id)
                    send_message(chat_id, f"{result}/5 correct answers. \n Enter /start if you would try again")
                else:
                    send_message(chat_id, question["questions"][len(answer_arr)]["question"])
    return {"ok": True}


if __name__ == "__main__":
    app.run()
