import lib.slack_client as slack_client
from dataclasses import dataclass
from typing import Optional
from lib.auth import Authorizer, UnauthorizedAction
from lib.user import User

@dataclass
class CommandData:
    """"""
    auth: Authorizer
    caller: User
    user: Optional[User]
    platform: Optional[str]

# class BotManager:
#     """Manager for bot activites including user mana"""
#     def __init__(self):
#         self.db = DatabaseAccess('build_database.db')
#         #self.slack = SlackManager()

def create_user(slack_id: str) -> User:
    """Create a new User object."""
    user = new_slack_user(slack_id)
    user.set_user_admin(user.user_id in db.admin_ids)
    user.set_user_platforms(db.get_owner_platforms(user.user_id))

    # COULD BE MOVED TO EVENT
    if user.get_user_platforms() == []:
        # Add new user to the User table
        db.add_user(user.user_id, user.name, user.email)
    return user

def new_slack_user(slack_id: str) -> User:
    """Get user info from Slack"""
    profile = slack_client.get_slack_info(slack_id)
    return User(**profile)

def register_owner(command: CommandData):
    """Add a user as an owner to a platform"""
    if command.auth.authorize():
        db.register_owner(command.user.userId, command.platform)
    else:
        raise UnauthorizedAction(caller=command.caller, 
            message=f"User {command.caller.name} ({command.caller.email}) does not have permission to register an owner for platform '{command.platform}'")

def delete_user(command:CommandData):
    """Removes a user from the database. All associated ownerships are deleted as well."""
    if command.auth.authorize():
        db.delete_user(command.user.userId)
    else:
        raise UnauthorizedAction(caller=command.caller, 
            message=f"User {command.caller.email} ({command.caller.name}) does not have permission to delete a user")