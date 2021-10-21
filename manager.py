"""Basically defunct file now. Moved all functionality to bot.py"""
import lib

# class BotManager:
#     """Manager for bot activites including user mana"""
#     def __init__(self):
#         self.db = DatabaseAccess('build_database.db')
#         #self.slack = SlackManager()


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