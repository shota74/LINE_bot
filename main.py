import urllib.request
import os
import sys
import json
import scrape as sc
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

channel_secret = os.getenv('LINE_CHANNEL_SECRET', d7cb389c9d0889a691a6f404ee4229f4)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', k5qSFVxKFT6qE34E9Osu9P/9ZwLZO/htMmdUOz3BQuAZVYI7I7fmH2S5ZGKUmzyyEpyWqEyeTww7LLCfjIaxCY66u5xM57OXMMhzvB6JF/m/r48DMLlpX8aDtPXOie5fRw20y+KEMqWssKNv1ngtiQdB04t89/1O/w1cDnyilFU=)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)


    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    word = event.message.text
    result = sc.getNews(word)

    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=result)
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
