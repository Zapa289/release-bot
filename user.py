from dataclasses import dataclass, field

@dataclass
class User:
    userId: str
    name: str
    email: str
    isAdmin: bool = field(init=False, default=False)
    ownedPlatforms: list[str] = field(init=False, default_factory=list)

    def set_admin(self, isAdmin: bool):
        self.isAdmin = isAdmin

    def set_platforms(self, platforms: list[str]):
        self.ownedPlatforms = platforms

    def get_platforms(self) -> list:
        return self.ownedPlatforms