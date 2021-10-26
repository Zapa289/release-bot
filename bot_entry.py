"""Core function of the release bot."""
import os
import json
from pathlib import Path

from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv

import slack_home
from lib import slack_client
from db_manager import SQLiteDatabaseAccess
from slack_action import ReleaseBot

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

APP_ID = "A026U9M6F2M"
#BOT_ID = client.api_call("auth.test")['user_id']

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SLACKBOT_SIGNING_SECRET'], '/slack/events', app)

database = SQLiteDatabaseAccess('test.db')

bot = ReleaseBot(database)

# @slack_event_adapter.on('message')
# def message_received(payload):
#     """Message event"""
#     event = payload.get('event', {})
#     channel_id = event.get('channel')
#     user_id = event.get('user')
#     text = event.get('text')
#     BOT_ID = lib.slack_client.client.api_call("auth.test")['user_id']

#     if user_id is not None and BOT_ID != user_id:
#         # if user_id in message_counts:
#         #     message_counts[user_id] += 1
#         # else:
#         #     message_counts[user_id] = 1

#         if channel_id == lib.slack_client.TEST_JENKINS_CHANNEL:
#             if text.lower() == "demo":
#                 #lib.jenkins.process_Jenkins(payload)
#                 pass

# @slack_event_adapter.on('reaction_added')
# def reaction_added(payload):
#     event = payload.get('event', {})
#     channel_id = event.get('item', {}).get('channel')
#     user_id = event.get('user')
#     used_on_id = event.get('item_user')

#     if channel_id != lib.slack_client.TEST_JENKINS_CHANNEL:
#         return
#     #
#     # check for user permission
#     #

@slack_event_adapter.on('app_home_opened')
def app_home_opened(payload):
    """User clicked the home tab"""
    event = payload.get('event', {})
    user_id = event.get('user')
    user = create_user(user_id)
    if not user:
        return Response(response="User not found"), 200

    home_blocks = slack_home.get_home_tab(user, db.platforms)

    slack_client.publish_view(user_id, home_blocks)

    return Response(), 200

@app.route('/actions', methods=['POST'])
def slack_action_entry():
    """Handles all actions from users"""

    if not slack_client.is_valid_request(request):
        return Response(response='Invalid request'), 200

    event = json.loads(request.form['payload'])

    bot.process_event(event)

    return Response(), 200

def main():
    """Start the bot"""
    app.run(debug=True)

if __name__ == "__main__":
    main()
