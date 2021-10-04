from auth import Authorizer
from typing import List
from db_manager import DatabaseAccess
from slack_client import SlackManager
from user import User

class BotManager:
    def __init__(self):
        self.db = DatabaseAccess('build_database.db')
        self.slack = SlackManager()

    def create_User(self, id: str) -> User:
        user = self.new_slack_user(id)
        user.set_admin(self.db.get_admin(user.userId))
        user.set_platforms(self.db.get_owner_platforms(user.userId))         

        # COULD BE MOVED TO EVENT
        if user.ownedPlatforms == []:
            # Add new user to the User table
            self.db.add_user(user.userId, user.name, user.email)
        return user

    def new_slack_user(self, id: str) -> User:
        profile = self.slack.get_slack_info(id)

        userId = self.slack.get_user_id(profile)
        name = self.slack.get_user_real_name(profile)
        email = self.slack.get_user_email(profile)

        return User(userId, name, email)


    def register_owner(self, owner: User, user: User, platform: str, auth: Authorizer):
        #
        # NEED TO DO AUTHORIZING
        #
        if auth.authorize(owner, platform):
            self.db.register_owner(user.userId, platform)

        user.ownedPlatforms = user.ownedPlatforms.append(platform)

    def delete_user(self, user: User):
        """Removes a user from the database"""
        ### Authorize deletion
        pass