import os
import json
from flask import Flask, request, Response
import lib.slack_client as slack_client
import manager
from lib.auth import AuthOwner, AuthAdmin, UnauthorizedAction
from lib.BuildMessage import BuildNotification, BuildMessage
from slackeventsapi import SlackEventAdapter

from pathlib import Path
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

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

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SLACKBOT_SIGNING_SECRET'], '/slack/events', app)

# def process_Jenkins(build_event):
#     event = build_event.get('event', {})
#     channel_id = event.get('channel')
#     #build_info = json.loads(event.get('text'))
#     build_info = json.loads(DEMO_JENKINS_MESSAGE)

#     message = 'I found a new build! ' +  str(build_info.get('new_rom_version','oops'))
#     slack_client.write_message(channel=channel_id, message=message)
#     build_message = BuildNotification(build_info).get_build_message()
#     #print(message)

#     for platform in build_info.get('platform'):
#         # build_log[platform][build_info.get('new_rom_version')] = build_message
#         # print(build_log[platform][build_info.get('new_rom_version')])
#         #db_manager.store_build_message(build_message)
#         slack_message = BuildMessage(build_message=build_message)

#     response = slack_client.client.chat_postMessage(channel=channel_id,**build_message)
#     build_message.timestamp = response['ts']
#     #
#     # log build message for later to update
#     #

@slack_event_adapter.on('message')
def message_received(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    BOT_ID = slack_client.client.api_call("auth.test")['user_id']

    if user_id is not None and BOT_ID != user_id:
        # if user_id in message_counts:
        #     message_counts[user_id] += 1
        # else:
        #     message_counts[user_id] = 1

        if channel_id == slack_client.TEST_JENKINS_CHANNEL:
            if text.lower() == "demo":
                #lib.jenkins.process_Jenkins(payload)
                pass

@slack_event_adapter.on('reaction_added')
def reaction_added(payload):
    event = payload.get('event', {})
    channel_id = event.get('item', {}).get('channel')
    user_id = event.get('user')
    used_on_id = event.get('item_user')

    if channel_id != slack_client.TEST_JENKINS_CHANNEL:
        return
    #
    # check for user permission
    #

@app.route('/release-bot', methods=['POST'])
def release_bot_commands():
    """Handles all commands from general users/owners"""

    if not slack_client.is_valid_request(request):
        return Response(response='Invalid request'), 200
    return Response(), 200

    event = request.form.to_dict()
    user_data = event['text']
    user_id = event['user_id']

    owner = manager.create_user(user_id)
    user = None
    platform = None

    command = manager.CommandData(
        AuthOwner(owner, platform),
        owner,
        user,
        platform
        )
    if 'help' in user_data:
        response = Response()

    try:
        manager.register_owner(command)
    except UnauthorizedAction as error:
        # Do error stuff (send an ephemeral message to the user perhaps)
        print(error.message)

        
def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
     