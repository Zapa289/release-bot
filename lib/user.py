from dataclasses import dataclass, field

@dataclass
class User:
    """Contains user information"""
    id: str
    name: str
    email: str
    is_admin: bool = field(init=False, default=False)
    owned_platforms: list[str] = field(init=False, default_factory=list)
    subscriptions: list[str] = field(init=False, default_factory=list)
