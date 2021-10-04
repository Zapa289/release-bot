from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    userId: str
    name: str
    email: str
    isAdmin: bool = field(init=False, default=False)
    ownedPlatforms: List[str] = field(init=False, default_factory=list)

    def set_admin(self, isAdmin: bool):
        self.isAdmin = isAdmin

    def set_platforms(self, platforms: List[str]):
        self.ownedPlatforms = platforms