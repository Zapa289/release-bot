import slack
import os
import json

from pathlib import Path
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from db_manager import BuildMessage, User



TEST_CHANNEL = 'C026CJB5MUM'
TEST_JENKINS_CHANNEL = 'C026QHP52EP'
TEST_JENKINS_BOT = 'C026QHP52EP' # my ID

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SLACKBOT_SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACKBOT_TOKEN'])

#BOT_ID = client.api_call("auth.test")['user_id']
DEMO_JENKINS_MESSAGE = """{
  "end_sha": "89c84c410f8670a15d73e6a90b3f8007efa01cf5",
  "start_sha": "eae54533244881c411add67a7f7b00b57a48584e",
  "branch": "origin/private/Jack/H10_05_27_2021",
  "platform": [
    "H10",
    "U47"
  ],
  "new_rom_version": "1.42_05_27_2021",
  "parent_rom_version": "1.42_04_30_2021",
  "snap": "Gen10 Plus Snap 4 Latent",
  "rom_type": "release",
  "bootleg_build_type": "DEBUG",
  "bootleg_desc": "",
  "user_email": "jack.tay.little@hpe.com",
  "release_doc_enabled": true,
  "debug_build_enabled": true,
  "release_build_enabled": true,
  "test_build_enabled": false,
  "skip_build_enabled": false,
  "submission_id": "49e2dd7b-ebf1-433b-b6fd-b7793264a485"
}
"""
#DEMO_PAYLOAD = {'event' : { 'channel' : TEST_JENKINS_CHANNEL, 'user' : BOT_ID, 'text' : DEMO_JENKINS_MESSAGE}}
# message_counts = {}
#build_log = {}

class BuildNotification:
    DIVIDER = {'type': 'divider'}

    def __init__(self, build_info):
        self.branch = build_info.get('branch')
        self.platforms = build_info.get('platform')
        self.new_rom_version = build_info.get('new_rom_version')
        self.parent_version = build_info.get('parent_rom_version')
        self.rom_type = build_info.get('rom_type')
        self.user_email = build_info.get('user_email')
        self.release = build_info.get('release_build_enabled')
        self.sub_id = build_info.get('submission_id')

        self.raw_json = build_info
        
        self.timestamp = ''
        self.is_prereleased = False

    def get_build_message(self):
        return { 
            'ts': self.timestamp,
            'blocks' : [
                #self.START_TEXT,
                self.DIVIDER,
                self._get_build_info(),
                self.DIVIDER,
                self._get_MAT_Status(),
                self.DIVIDER
            ] 
        }

    def _get_MAT_Status(self):
        checkmark = ':x:'
        if self.is_prereleased:
            checkmark = ':white_check_mark:'

        text = f'*Pre-released to Morpheus* {checkmark} '
        return {
            'type': 'section',
            'text': {
                'type' : 'mrkdwn',
                'text': text
            }
        }
    
    def _get_build_info(self):
        if len(self.platforms) > 1:
            text = '*'
            for platform in self.platforms:
                if self.platforms.index(platform) != 0:
                    text += ', '
                text += f'{platform}'
            text += ' builds complete*\n'
        else: 
            text =  f'*{self.platforms[0]} build complete*\n'
        text = text + f'Build version: {self.new_rom_version}'
        return {
            'type': 'section',
            'text': {
                'type' : 'mrkdwn',
                'text'  : text
            }
        }    

def process_Jenkins(build_event):
    event = build_event.get('event', {})
    channel_id = event.get('channel')
    #build_info = json.loads(event.get('text'))
    build_info = json.loads(DEMO_JENKINS_MESSAGE)  
  
    client.chat_postMessage(channel=channel_id, text='I found a new build! ' +  str(build_info.get('new_rom_version','oops')))
    build_message = BuildNotification(build_info).get_build_message()
    #print(message)

    for platform in build_info.get('platform'):
        # build_log[platform][build_info.get('new_rom_version')] = build_message
        # print(build_log[platform][build_info.get('new_rom_version')])
        #db_manager.store_build_message(build_message)
        slack_message = BuildMessage(build_info=build_message)

    response = client.chat_postMessage(channel=channel_id,**build_message)
    build_message.timestamp = response['ts']
    #
    # log build message for later to update
    #
    


@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    BOT_ID = client.api_call("auth.test")['user_id']

    if user_id != None and BOT_ID != user_id:
        # if user_id in message_counts:
        #     message_counts[user_id] += 1
        # else:
        #     message_counts[user_id] = 1

        if channel_id == TEST_JENKINS_CHANNEL:
            if text.lower() == "demo":
                process_Jenkins(payload)

@slack_event_adapter.on('reaction_added')
def reaction_added(payload):
    event = payload.get('event', {})
    channel_id = event.get('item', {}).get('channel')
    user_id = event.get('user')
    used_on_id = event.get('item_user')

    if channel_id != TEST_JENKINS_CHANNEL:
        return
    #
    # check for user permission
    #




# @app.route('/message-count', methods=['POST'])
# def message_count():
#     data = request.form
#     user_id = data.get('user_id')
#     channel_id = data.get('channel_id')

#     if user_id in message_counts:
#         client.chat_postMessage(channel=channel_id, text=f'Message Count: {message_counts[user_id]}')
#     return Response(), 200

@app.route('/register-Owner', methods=['POST'])
def register_owner():
    data = request.form
    userData = data.get('text')
    user_id = data.get('user_id')

    if 'help' in userData:
        response = Response()


if(__name__ == "__main__"):
    app.run(debug=True)
     