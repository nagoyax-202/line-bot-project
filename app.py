from flask import Flask, request, abort
import os
import requests

app = Flask(__name__)

# LINE Bot のチャネルアクセストークン（コード内に直接記述する場合）
LINE_CHANNEL_ACCESS_TOKEN = 'ここにあなたのチャネルアクセストークンを貼ってください'

# ヘッダーの準備（LINEのAPIを呼ぶために必要）
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
}

@app.route("/")
def hello():
    return "LINE Bot Flask App is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json

    # メッセージイベントがあったとき
    if "events" in body:
        for event in body["events"]:
            if event["type"] == "message" and event["message"]["type"] == "text":
                reply_token = event["replyToken"]
                user_message = event["message"]["text"]

                reply_message = {
                    "replyToken": reply_token,
                    "messages": [
                        {"type": "text", "text": f"あなたは「{user_message}」と書きましたね！"}
                    ]
                }

                requests.post(
                    "https://api.line.me/v2/bot/message/reply",
                    headers=headers,
                    json=reply_message
                )

    return "OK", 200

# ↓ここがRenderで動かすために「必ず」必要な部分です
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
