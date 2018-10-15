from flask import Flask, request, jsonify
from api import Api
# If your domain has no "https" then uncomment the code below (maybe it will help you)
# from flask_sslify import SSLify

app = Flask(__name__)
# sslify = SSLify(app)
ai_bot = Api()


def controller():
    r = request.get_json()
    chat_id = r['message']['chat']['id']
    ai_bot.write_json(r, 'telegram.json')
    fulfillment_text = ai_bot.detect_texts(ai_bot.DIALOGFLOW_PROJECT_ID, 'unique', r['message']['text'], 'en')
    ai_bot.send_message(chat_id, fulfillment_text)
    return jsonify(r)


@app.route('/', methods=['POST', 'GET'])
def main():

    if request.method == 'POST':
        controller()
    r = ai_bot.getwebhook_info()
    if not r['result']['url']:
        ai_bot.setwebhook()
    return "<h2>It's done</h2>"


if __name__ == '__main__':
    app.run()

