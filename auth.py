from enum import Enum
from abc import ABC, abstractmethod
from dataclasses import dataclass

from user import User

class Authorizer(ABC):
    def __init__(self, owner: User):
        self.owner = owner
        self.platform = platform

    @abstractmethod
    def authorize(self) -> bool:
        pass

class AuthAdmin(Authorizer):
    def authorize(self) -> bool:
        return self.owner.isAdmin

class AuthOwner(Authorizer):
    def __init__(self, platform):
        self.platform = platform

    def authorize(self) -> bool:
        return self.owner.isAdmin or (self.platform in self.owner.ownedPlatforms) 



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

class AuthLevel(Enum):
    admin = "admin"
    owner = 'owner'

@dataclass
class AuthStruct:
    owner: User
    platform : str = None

class Auth:
    def __init__(self):
        #Authentication dispatcher
        self.auth_func = {
            AuthLevel.admin : self.auth_admin,
            AuthLevel.owner : self.auth_owner
        }

    def auth(self, authLevel: AuthLevel, owner: User, platform: str = None) -> bool:
        """Dispatcher for required Authentication Level"""
        try:
            return self.auth_func[authLevel](AuthStruct(owner, platform))
        except KeyError:
            #Invalid AuthLevel
            return False

    def auth_admin(self, data: AuthStruct) -> bool:
        """Return if user has Admin rights"""
        return data.owner.isAdmin

    def auth_owner(self, data: AuthStruct) -> bool:
        """Return if user owns a platform or is an Admin"""
        return data.owner.isAdmin or (data.platform in data.owner.ownedPlatforms) 
        if not data.owner.isAdmin and (data.platform not in data.user.ownedPlatforms):
            return False
            #raise UnauthorizedAction(message=f'User {owner.name} ({owner.userId}) does not have permission to register a user to platform "{platform}"')
            
        # if data.platform in data.owned_platforms:
        #     raise UserAlreadyOwner(userId=user.userId, platform=platform, message=f'User {user.name} (ID: {user.userId}) is already an owner of platform "{platform}"')
