import os
from flask.wrappers import Request
from flask import Flask
import slack
from slack.signature.verifier import SignatureVerifier
from slackeventsapi import SlackEventAdapter

from pathlib import Path
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

TEST_CHANNEL = 'C026CJB5MUM'
TEST_JENKINS_CHANNEL = 'C026QHP52EP'
TEST_JENKINS_BOT = 'U026CK3BVD3' # my ID
MY_ID = "U0260T4PKPZ"

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SLACKBOT_SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACKBOT_TOKEN'])

slack_verifier = SignatureVerifier(os.environ['SLACKBOT_SIGNING_SECRET'])

def is_valid_request(event: Request) -> bool:
    """Return if event is a valid Slack request"""
    return slack_verifier.is_valid_request(event.get_data(), event.headers)

def get_slack_info(user_id: str) -> dict[str, str]:
    """Gets information about a user from Slack"""

    user_info = client.users_identity(user=user_id)
    if not user_info.get('ok'):
        raise UserNotFound(user_id=user_id, message=f"User ({user_id}) could not be found. Error: {user_info.get('error')}")

    return user_info.get('user')

def get_user_id_from_profile(profile: dict[str, str]) -> str:
    """Get the user ID from the slack user profile"""
    return profile.get('id')

def get_user_email_from_profile(profile: dict[str, str]) -> str:
    """Get the user email from the slack user profile"""
    return profile.get('email')

def get_user_name_from_profile(profile: dict[str, str]) -> str:
    """Get the user's name from the slack user profile"""
    return profile.get('name')

def write_message(channel: str, message: str):
    client.chat_postMessage(channel=channel, text=message)


class UserNotFound(Exception):
    """Custom exception for when Slack users_info """
    def __init__(self, user_id: str, message='Could not find user.'):
        self.user_id = user_id
        self.message = message
        super().__init__(self.message)