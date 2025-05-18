from flask import Flask, request
import requests
import os

app = Flask(__name__)

# あなたのチャネルアクセストークンをここに貼ってください
LINE_TOKEN = "ここにペースト！"

@app.route("/")
def home():
    return "VQfufkIZoWjkUSZUvzz9HrkJkbRoaDlRmu6FWktuMXqjpm3WRWyw/RwEcQ4wCyKdgviivyQGSbOqhrr4Pf3kQkKe3xQ3vtGhb7oPVQnwWSapJNrBvnGaDWIDGYR5Bfo6afJs5Zq4UFyEcPI2D0qeXQdB04t89/1O/w1cDnyilFU="

@app.route("/callback", methods=["POST"])
def callback():
    body = request.json
    try:
        event = body["events"][0]
        reply_token = event["replyToken"]
        user_message = event["message"]["text"]

        reply_message = f"『{user_message}』って言ったね！"

        headers = {
            "Authorization": f"Bearer {LINE_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "replyToken": reply_token,
            "messages": [
                {
                    "type": "text",
                    "text": reply_message
                }
            ]
        }

        requests.post("https://api.line.me/v2/bot/message/reply",
                      headers=headers, json=payload)

        return "OK"

    except Exception as e:
        print("エラー:", e)
        return "NG"

if __name__ == "__main__":
    app.run()
