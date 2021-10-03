from typing import Dict
import slack
import os

from pathlib import Path
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

from flask import Flask
from slackeventsapi import SlackEventAdapter

TEST_CHANNEL = 'C026CJB5MUM'
TEST_JENKINS_CHANNEL = 'C026QHP52EP'
TEST_JENKINS_BOT = 'C026QHP52EP' # my ID

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SLACKBOT_SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACKBOT_TOKEN'])

class SlackManager:
    def get_slack_info(self, id: str) -> Dict[str, str]:
        """Gets the profile data from the slack users_info API"""

        userInfo = client.users_info(user=id)
        userProfile = userInfo.get('profile', "")

        return userProfile

    def get_user_id(self, profile: Dict[str, str]) -> str:
        """Get the user ID from the slack user profile"""
        return profile.get('id')

    def get_user_email(self, profile: Dict[str, str]) -> str:
        """Get the user email from the slack user profile"""
        return profile.get('email')
    
    def get_user_real_name(self, profile: Dict[str, str]) -> str:
        """Get the user's name from the slack user profile"""
        return profile.get('real_name')

    def write_message(self, channel: str, message: str):
        client.chat_postMessage(channel=channel, text=message)