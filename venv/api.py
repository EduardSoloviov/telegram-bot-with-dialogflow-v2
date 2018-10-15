import os
import requests, json
from dotenv import load_dotenv

from google.cloud import storage
import dialogflow_v2 as dialogflow

# from subprocess import call


class Api:

    DOTENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(DOTENV_PATH)
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    URL = "https://api.telegram.org/bot%s/" % TOKEN
    HOST_URL = os.getenv("HOST_URL")
    DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    def __init__(self):
        self._auth()

    def write_json(self, data, filename='response.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def detect_texts(self, project_id, session_id, text, lang_code):
        session_client = dialogflow.SessionsClient.from_service_account_json(self.GOOGLE_APPLICATION_CREDENTIALS)
        session = session_client.session_path(project_id, session_id)

        if text:
            text_input = dialogflow.types.TextInput(text=text, language_code=lang_code)
            query_input = dialogflow.types.QueryInput(text=text_input)
            response = session_client.detect_intent(session=session, query_input=query_input)
            return response.query_result.fulfillment_text

    def getwebhook_info(self):
        url = self.URL + 'getWebhookInfo'
        r = requests.post(url)
        return r.json()

    def send_message(self, chat_id, text="i can't get you"):
        url = self.URL + 'sendMessage'
        response = {'chat_id': chat_id, 'text': text}
        r = requests.post(url, json=response)
        return r.json()

    def _auth(self):
        storage_client = storage.Client.from_service_account_json(self.GOOGLE_APPLICATION_CREDENTIALS)
        buckets = list(storage_client.list_buckets())
        print(buckets)

    def setwebhook(self):
        print('{}setWebhook?url={}'.format(self.URL, self.HOST_URL))
        r = requests.post('{}setWebhook?url={}'.format(self.URL, self.HOST_URL))
        print(r.json())
        # If the way above doesn't work, uncomment the one below...by the way don't forget uncomment import
        # call(["curl ", "-X", " POST ",
        #       "{}setWebhook?url={}".format(self.URL, self.HOST_URL)], shell=True)

