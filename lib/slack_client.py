import os
from pathlib import Path

from flask.wrappers import Request
from slack import WebClient
from slack.errors import SlackApiError
from dotenv import load_dotenv

from lib.user import User
from slack.signature.verifier import SignatureVerifier

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

TEST_CHANNEL = 'C026CJB5MUM'
TEST_JENKINS_CHANNEL = 'C026QHP52EP'
TEST_JENKINS_BOT = 'U026CK3BVD3' # my ID
MY_ID = "U0260T4PKPZ"

client = WebClient(token=os.environ['SLACKBOT_TOKEN'])
slack_verifier = SignatureVerifier(os.environ['SLACKBOT_SIGNING_SECRET'])

def is_valid_request(event: Request) -> bool:
    """Return if event is a valid Slack request"""
    return slack_verifier.is_valid_request(event.get_data(), event.headers)

def new_slack_user(slack_id: str) -> User:
    """Get user info from Slack"""
    try:
        profile = get_slack_info(slack_id)
    except UserNotFound as error:
        print(error)
        raise error

    user_id = profile["id"]
    email = profile["profile"]["email"]
    name = profile["real_name"]
    return User(id=user_id, name=name, email=email)

def get_slack_info(user_id: str) -> dict[str, str]:
    """Gets information about a user from Slack"""
    user_info = {}
    try:
        user_info = client.users_info(user=user_id)
    except SlackApiError as error:
        error_response = error.response['error']
        print(error.response)

    if not user_info.get('ok'):
        raise UserNotFound(user_id=user_id, message=f"User ({user_id}) could not be found. Error: {error_response}")

    return user_info.get('user')

def write_message(channel: str, message: str):
    client.chat_postMessage(channel=channel, text=message)

def publish_view(user_id: str, blocks: dict):
    response = client.views_publish(user_id=user_id, view=blocks)

    if not response['ok']:
        raise SlackResponseError(user_id=user_id, message=f"Error during view.publish: {response['error']}")

def create_new_release_channel(channel_name: str) -> str:
    """Create a new slack channel for releases. Returns channel ID"""
    try:
        response = client.conversations_create(name=channel_name)
    except SlackApiError as error:
        print(error)

    if not response["ok"]:
        #do some logging
        print(f"Error creating channel '{channel_name}''. Error: {response['error']}")
        return None

    channel = response["channel"]
    return channel['id']

def open_modal(trigger_id, modal):
    """Opens a modal"""
    try:
        response = client.views_open(trigger_id=trigger_id, view=modal)
    except SlackApiError as error:
        print(error.response)



class UserNotFound(Exception):
    """Custom exception for when Slack users_info """
    def __init__(self, user_id: str, message: str ='Could not find user.'):
        self.user_id = user_id
        self.message = message
        super().__init__(self.message)

class SlackResponseError(Exception):
    """Custom exception for when Slack gives an error response"""
    def __init__(self, user_id: str, message: str = "Slack responded with an error!"):
        self.user_id = user_id
        self.message = message
        super().__init__(message)