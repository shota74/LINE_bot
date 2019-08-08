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
import os

app = Flask(__name__)


#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["k5qSFVxKFT6qE34E9Osu9P/9ZwLZO/htMmdUOz3BQuAZVYI7I7fmH2S5ZGKUmzyyEpyWqEyeTww7LLCfjIaxCY66u5xM57OXMMhzvB6JF/m/r48DMLlpX8aDtPXOie5fRw20y+KEMqWssKNv1ngtiQdB04t89/1O/w1cDnyilFU="]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["d7cb389c9d0889a691a6f404ee4229f4"]

line_bot_api = LineBotApi('k5qSFVxKFT6qE34E9Osu9P/9ZwLZO/htMmdUOz3BQuAZVYI7I7fmH2S5ZGKUmzyyEpyWqEyeTww7LLCfjIaxCY66u5xM57OXMMhzvB6JF/m/r48DMLlpX8aDtPXOie5fRw20y+KEMqWssKNv1ngtiQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d7cb389c9d0889a691a6f404ee4229f4')

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        #TextSendMessage(text=event.message.text))
        TextSendMessage(text="hoge"))



if __name__ == "__main__":
    #app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
