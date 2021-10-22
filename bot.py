"""Core function of the release bot."""
import os
from pathlib import Path
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv
import slack_home
import lib
from db_manager import SQLiteDatabaseAccess


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

APP_ID = "A026U9M6F2M"
#BOT_ID = client.api_call("auth.test")['user_id']

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SLACKBOT_SIGNING_SECRET'], '/slack/events', app)
db = SQLiteDatabaseAccess('test.db')

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

    home_blocks = slack_home.get_home_tab(user, db)

    lib.slack_client.publish_view(user_id, home_blocks)

    return Response(), 200

@app.route('/action', methods=['POST'])
def slack_action():
    """Handles all actions from users"""

    if not lib.slack_client.is_valid_request(request):
        return Response(response='Invalid request'), 200

    event = request.form.to_dict()

    #check what action prompted the event

    #create proper modal

    #send up the modal

    return Response(), 200

@app.route('/release-bot', methods=['POST'])
def release_bot_commands():
    """Handles all commands from general users/owners"""

    if not lib.slack_client.is_valid_request(request):
        return Response(response='Invalid request'), 200
    return Response(), 200

    # event = request.form.to_dict()
    # user_data = event['text']
    # user_id = event['user_id']

    # owner = create_user(user_id)
    # user = None
    # platform = None

    # command = manager.CommandData(
    #     AuthOwner(owner, platform),
    #     owner,
    #     user,
    #     platform
    #     )
    # if 'help' in user_data:
    #     response = Response()

    # try:
    #     manager.register_owner(command)
    # except UnauthorizedAction as error:
    #     # Do error stuff (send an ephemeral message to the user perhaps)
    #     print(error.message)

def create_user(slack_id: str) -> lib.User:
    """Create a new User object."""
    user: lib.User = lib.slack_client.new_slack_user(slack_id)
    user.is_admin = user.id in db.admin_ids
    user.owned_platforms = db.get_owner_platforms(user.id)
    user.subscriptions = db.get_user_subscriptions(user.id)

    # COULD BE MOVED TO EVENT
    # if user.get_user_platforms() == []:
    #     # Add new user to the User table
    #     db.add_user(user.id, user.name, user.email)
    return user

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
