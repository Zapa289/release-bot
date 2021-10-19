from dataclasses import dataclass, field

@dataclass
class Platform:
    """Describes a ROM platform"""
    rom_family: str
    description : str = field(default='', compare=False)
    slack_channel: str = field(default='', compare=False)

class PlatformNotFound(Exception):
    def __init__(self, message="Could not find requested platform in databse"):
        self.message = message
        super().__init__(self.message)