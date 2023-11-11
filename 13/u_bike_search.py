from flask import Flask, request, abort,jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os


app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

# get api
@app.route("/TT", methods=['GET'])
def TT():
    return jsonify(message='OK')
# post api
@app.route("/around_search", methods=['POST'])
def around_search():
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
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)

    # https://hackmd.io/@shaoeChen/HJiZtEngG/https%3A%2F%2Fhackmd.io%2F%40shaoeChen%2FBkL3oACzU
    # https://molly1024.medium.com/python-%E8%88%87-line-bot-%E5%BE%9E%E9%A0%AD%E9%96%8B%E5%A7%8B%E5%BB%BA%E7%AB%8B%E4%B8%80%E5%80%8B-line-%E6%A9%9F%E5%99%A8%E4%BA%BA-%E9%83%A8%E7%BD%B2%E5%88%B0-heroku-51512b04cb7b