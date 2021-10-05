from enum import Enum
from abc import ABC, abstractmethod
from dataclasses import dataclass

from user import User

class Authorizer(ABC):
    @abstractmethod
    def authorize(self) -> bool:
        pass

class AuthAdmin(Authorizer):
    """Authorize caller as Admin"""
    def __init__(self, caller: User):
        self.caller = caller

    def authorize(self) -> bool:
        return self.caller.isAdmin

class AuthOwner(Authorizer):
    """Authorize caller as Admin or owner of a platform"""
    def __init__(self, caller: User, platform):
        self.caller = caller
        self.platform = platform

    def authorize(self) -> bool:
        return self.caller.isAdmin or (self.platform in self.caller.ownedPlatforms) 



class UnauthorizedAction(Exception):
    """Custom exception for when a caller does not have permission to perform an action"""
    def __init__(self, caller: User, message='You do not have permisson to do that'):
        self.caller = caller
        self.message = message
        super().__init__(self.message)

class UserAlreadyOwner(Exception):
    """Custom exception for when a user is being assigned a platform they already own"""
    def __init__(self, userId, platform, message='User is already an owner of that platform'):
        self.message = message
        self.userId = userId
        self.platform = platform
        super().__init__(self.message)

# class AuthLevel(Enum):
#     admin = "admin"
#     owner = 'owner'

# @dataclass
# class AuthStruct:
#     owner: User
#     platform : str = None

# class Auth:
#     def __init__(self):
#         #Authentication dispatcher
#         self.auth_func = {
#             AuthLevel.admin : self.auth_admin,
#             AuthLevel.owner : self.auth_owner
#         }

#     def auth(self, authLevel: AuthLevel, owner: User, platform: str = None) -> bool:
#         """Dispatcher for required Authentication Level"""
#         try:
#             return self.auth_func[authLevel](AuthStruct(owner, platform))
#         except KeyError:
#             #Invalid AuthLevel
#             return False

#     def auth_admin(self, data: AuthStruct) -> bool:
#         """Return if user has Admin rights"""
#         return data.owner.isAdmin

#     def auth_owner(self, data: AuthStruct) -> bool:
#         """Return if user owns a platform or is an Admin"""
#         return data.owner.isAdmin or (data.platform in data.owner.ownedPlatforms) 
#         if not data.owner.isAdmin and (data.platform not in data.user.ownedPlatforms):
#             return False
#             #raise UnauthorizedAction(message=f'User {owner.name} ({owner.userId}) does not have permission to register a user to platform "{platform}"')
            
#         # if data.platform in data.owned_platforms:
#         #     raise UserAlreadyOwner(userId=user.userId, platform=platform, message=f'User {user.name} (ID: {user.userId}) is already an owner of platform "{platform}"')
