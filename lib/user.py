from dataclasses import dataclass, field

@dataclass
class User:
    """Contains user information"""
    user_id: str
    name: str
    email: str
    is_admin: bool = field(init=False, default=False)
    owned_platforms: list[str] = field(init=False, default_factory=list)

    def set_user_admin(self, is_admin: bool):
        """Set user's admin status"""
        self.is_admin = is_admin

    def get_user_admin(self) -> bool:
        """Get user's admin status"""
        return self.is_admin

    def set_user_platforms(self, platforms: list[str]):
        """Sets a user's list of owned platformsplatforms"""
        self.owned_platforms = platforms

    def get_user_platforms(self) -> list[str]:
        return self.owned_platforms
