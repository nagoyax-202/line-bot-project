from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os

# 環境変数でセキュリティ確保する場合（今回は直接埋め込み）
# CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
# CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

app = Flask(__name__)

# ↓ここにあなたのチャネルアクセストークンとシークレットを貼り付けてください
line_bot_api = LineBotApi("VQfufkIZoWjkUSZUvzz9HrkJkbRoaDlRmu6FWktuMXqjpm3WRWyw/RwEcQ4wCyKdgviivyQGSbOqhrr4Pf3kQkKe3xQ3vtGhb7oPVQnwWSapJNrBvnGaDWIDGYR5Bfo6afJs5Zq4UFyEcPI2D0qeXQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("1718d312f275bd4a7c3febcc988671a5")


@app.route("/")
def home():
    return "LINE Bot Flask App is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ユーザーから受け取ったメッセージを取得
    user_message = event.message.text

    # 応答メッセージを作成（例：オウム返し）
    reply_text = f"「{user_message}」を受け取りました！"

    # 応答を送信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )


if __name__ == "__main__":
    app.run()
