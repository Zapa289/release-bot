from typing import List
from db_manager import DatabaseAccess
from slack_client import SlackManager
from dataclasses import dataclass, field

@dataclass
class User:
    userId: str
    name: str
    email: str
    isAdmin: bool = field(init=False, default=False)
    ownedPlatforms: List[str] = field(init=False, default_factory=[])

    def set_admin(self, isAdmin: bool):
        self.isAdmin = isAdmin

    def set_platforms(self, platforms: List[str]):
        self.ownedPlatforms = platforms

class UnauthorizedAction(Exception):
    def __init__(self, message='You do not have permisson to do that'):
        self.message = message
        super().__init__(self.message)

class UserAlreadyOwner(Exception):
    def __init__(self, userId, platform, message='User is already an owner of that platform'):
        self.message = message
        self.userId = userId
        self.platform = platform
        super().__init__(self.message)

class UserManager:
    def __init__(self):
        self.db = DatabaseAccess()
        self.slack = SlackManager()
        self.adminIds = self.db.get_admin_list()

    def create_User(self, id: str) -> User:
        user = self.new_slack_user(id)
        user.set_admin(id in self.adminIds)
        user.set_platforms(self.db.get_owner_platforms(id))

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


    def register_owner(self, owner: User, user: User, platform: str):
        #
        # NEED TO DO AUTHORIZING
        #
        if not owner.is_admin and (platform not in user.ownedPlatforms):
            raise UnauthorizedAction(message=f'User {owner.name} ({owner.userId}) does not have permission to register a user to platform "{platform}"')
            
        if platform in user.ownedPlatforms:
            raise UserAlreadyOwner(userId=user.userId, platform=platform, message=f'User {user.name} (ID: {user.userId}) is already an owner of platform "{platform}"')

        self.db.register_owner(user.userId, platform)

        user.ownedPlatforms = user.ownedPlatforms.append(platform)

    def delete_user(self, user: User):
        """Removes a user from the database"""
        ### Authorize deletion

        