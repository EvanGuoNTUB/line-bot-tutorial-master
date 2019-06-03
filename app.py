from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('CDRIHIRic7tDwJuuEuAR//z8qbb7YMu413TRKslobqs9cc9mXS5RMJ8VrpgGwqkDVmc/7XGiv8S2ndhJIPlnF7K7d0y4lF81/ulcooaeu9zSpbGpwKJZexc8D//OL0QKdSqIVQeXRIp9K7n+1dwn/wdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('20fd7339fc2682668274877a87c2aba7')

# 監聽所有來自 /callback 的 Post Request
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
