import time

import gspread
from flask import Flask
from flask import request, jsonify
import os
import dialogflow
import requests
from google.api_core.exceptions import InvalidArgument

import gsheet
from twilio.twiml.messaging_response import MessagingResponse
from PIL import Image

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

DIALOGFLOW_PROJECT_ID = 'local-services-yhur'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'
app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def root():
    # home()
    return "hello world"


def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)


@app.route('/api/getMessage', methods=['POST'])
def home():
    message = request.form.get('Body')
    mobnum = request.form.get('From')
    media_url = request.form.get('MediaUrl0')

    # if media_url:
    #     gc = gspread.service_account(filename='private_key.json')
        # wks = gc.open("SwastikJewellery").sheet1
        # code = wks.get("A:A")
        # col_a = len(wks.get("A:A")) + 1
        # col_b = len(wks.get('B:B')) + 1
        # col_c = len(wks.get("C:C")) + 1
        # filename = int(code[len(code) - 1][0]) + 1
        #
        # pr = price(mobnum)
        # print("in home after pr")
        # wks.update('A{0}'.format(col_a), filename)
        # wks.update('B{0}'.format(col_b), pr)
        # wks.update('C{0}'.format(col_c), media_url)
        # return respond('Thank you! Your image was received.')

        #     im = Image.open(media_url)
        #     im.show()
        #     r = requests.get(media_url)
        #     content_type = r.headers['Content-Type']
        #     username = mobnum.split(':')[1]  # remove the whatsapp: prefix from the number
        #     if content_type == 'image/jpeg':
        #         filename = 'uploads/.jpg'
        #     elif content_type == 'image/png':
        #         filename = 'uploads/.png'
        #     elif content_type == 'image/gif':
        #         filename = 'uploads/.gif'
        #     else:
        #         filename = None
        #     with open('uploads/', 'wb') as f:
        #         f.write(r.content)
        #
        #         # if not os.path.exists(f'uploads'):
        #         #     os.mkdir(f'uploads/{username}')
        #         # with open(filename, 'wb') as f:
        #         #     f.write(r.content)
    # # else:
    # return respond(f'Please send an image!')

    # print(message)
    # if(message=="price" or  "code" in message ):
    #     price(
    #         message,mobnum
    #     )

    if media_url:
        r = requests.get(media_url)
        content_type = r.headers['Content-Type']
        username = mobnum.split(':')[1]  # remove the whatsapp: prefix from the number
        if content_type == 'image/jpeg':
            filename = f'uploads/{username}/{message}.jpg'
        elif content_type == 'image/png':
            filename = f'uploads/{username}/{message}.png'
        elif content_type == 'image/gif':
            filename = f'uploads/{username}/{message}.gif'
        else:
            filename = None
        if filename:
            if not os.path.exists(f'uploads/{username}'):
                os.mkdir(f'uploads/{username}')
            with open(filename, 'wb') as f:
                f.write(r.content)
            return respond('Thank you! Your image was received.')
        else:
            return respond('The file that you submitted is not a supported image type.')
    else:
        return respond('Please send an image!')
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=message, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        # print("in home try")
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        # print("in home except")
        raise
    print("Query text:", response.query_result.query_text)
    print("Detected intent:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    print("Fulfillment text:", response.query_result.fulfillment_text)
    sendMessage(mobnum, response.query_result.fulfillment_text)
    return response.query_result.fulfillment_text


def price(mobnum):
    sendMessage(mobnum, "Please Enter The Price: ")
    message = request.values.get('Body')
    mobnum = request.form.get('From')
    print(message)
    return message


def sendMessage(mobnum, message):
    url = "https://api.twilio.com/2010-04-01/Accounts/ACaf43f3be48433f26189df20f842387fe/Messages.json"
    newmobnum = "whatsapp:+91"
    newmobnum = newmobnum + mobnum
    print(mobnum)
    payload = {'From': 'whatsapp:+14155238886',
               "Body": message,
               'To': mobnum}
    headers = {
        'Authorization': "Basic QUNhZjQzZjNiZTQ4NDMzZjI2MTg5ZGYyMGY4NDIzODdmZTo0ZTdmMTgyMTM1OWM1MGQ3YjdlMGQ4YmE2NzYxNmM3Zg=="
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text.encode('utf8'))
    return response.text.encode('utf8')


# def price(message,mobnum):
#     sendMessage(mobnum, "Please enter the code of the image")
#     # time.delay(10)
#     code = request.form.get('Body')
#     code.lower()
# pr=gsheet.pricegetter(code)
# sendMessage(mobnum,pr)


if __name__ == '__main__':
    # app.run()
    app.run(host='0.0.0.0', port=80)
