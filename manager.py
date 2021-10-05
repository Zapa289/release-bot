from dataclasses import dataclass
from typing import Optional
from auth import Authorizer, UnauthorizedAction
from db_manager import DatabaseAccess
from slack_client import SlackManager
from user import User

@dataclass
class CommandData:
    auth: Authorizer
    caller: User
    user: Optional[User]
    platform: Optional[str]

class BotManager:
    def __init__(self):
        self.db = DatabaseAccess('build_database.db')
        self.slack = SlackManager()

    def create_User(self, id: str) -> User:
        user = self.new_slack_user(id)
        user.set_admin(self.db.get_admin(user.userId))
        user.set_platforms(self.db.get_owner_platforms(user.userId))         

        # COULD BE MOVED TO EVENT
        if user.get_platforms() == []:
            # Add new user to the User table
            self.db.add_user(user.userId, user.name, user.email)
        return user

    def new_slack_user(self, id: str) -> User:
        profile = self.slack.get_slack_info(id)

        userId = self.slack.get_user_id(profile)
        name = self.slack.get_user_real_name(profile)
        email = self.slack.get_user_email(profile)

        return User(userId, name, email)


    def register_owner(self, c: CommandData):
        if c.auth.authorize():
            self.db.register_owner(c.user.userId, c.platform)
        else:
            raise UnauthorizedAction(caller=c.caller, message=f"User {c.caller.email} ({c.caller.name}) does not have permission to register an owner for platform '{c.platform}'")

        c.user.ownedPlatforms = c.user.ownedPlatforms.append(c.platform)

    def delete_user(self, user: User):
        """Removes a user from the database"""
        ### Authorize deletion
        pass