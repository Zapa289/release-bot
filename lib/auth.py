"""Authenticator for database accesses"""
from abc import ABC, abstractmethod
from lib.user import User

class Authorizer(ABC):
    """Abstract class for authorizing commands"""
    @abstractmethod
    def authorize(self) -> bool:
        """Authorize that user is authorized to use a command"""

class AuthAdmin(Authorizer):
    """Authorize caller as Admin"""
    def __init__(self, caller: User):
        self.caller = caller

    def authorize(self) -> bool:
        return self.caller.is_admin

class AuthOwner(Authorizer):
    """Authorize caller as Admin or owner of a platform"""
    def __init__(self, caller: User, platform):
        self.caller = caller
        self.platform = platform

    def authorize(self) -> bool:
        return self.caller.is_admin or (self.platform in self.caller.owned_platforms)



class UnauthorizedAction(Exception):
    """Custom exception for when a caller does not have permission to perform an action"""
    def __init__(self, caller: User, message='You do not have permisson to do that'):
        self.caller = caller
        self.message = message
        super().__init__(self.message)

class UserAlreadyOwner(Exception):
    """Custom exception for when a user is being assigned a platform they already own"""
    def __init__(self, user_id, platform, message='User is already an owner of that platform'):
        self.message = message
        self.user_id = user_id
        self.platform = platform
        super().__init__(self.message)
