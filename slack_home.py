import json
from lib.platform import Platform
import lib.slack_repo as sr
from lib.user import User
from db_manager import DatabaseAccess, PlatformNotFound

def get_home_tab(user: User, db : DatabaseAccess) -> str:
    """Generate the Hope tab for a user"""

    sub_blocks: list = get_subscription_blocks(user, db)

    if not sub_blocks:
        sub_blocks = sr.EMPTY_SUBSCRIPTION

    home_tab = {
	"type": "home",
	"blocks": [sr.SUBSCRIPTION_HEADER,
            sr.NEW_SUBSCRIPTION_BUTTON,
            sr.DIVIDER,
            sub_blocks
            ]
    }

    return json.dumps(home_tab)

def get_subscription_blocks(user: User, db: DatabaseAccess) -> list:
    """Get all the slack blocks for different """
    sub_blocks = list[dict]

    for platform in user.subscriptions:
        try:
            platform_info = db.get_platform(platform)
        except PlatformNotFound as error:
            #log stuff
            print(error.message)
            continue

        sub_blocks.append(new_subscription_block(platform_info))
        sub_blocks.append(new_context_block(platform_info))
        sub_blocks.append(sr.DIVIDER)

    return sub_blocks

def new_subscription_block(platform: Platform) -> dict:
    """Create a new subscription block cooresponding to the platform"""
    new_block = sr.SUBSCRIPTION
    new_block["text"]["text"] = f"*{platform.rom_family} ROM*\n{platform.description}"
    new_block["accessory"]["action_id"] = sr.SUB_ACTION_BASE + platform.rom_family

    return new_block

def new_context_block(platform: Platform) -> dict:
    """Create a new helper text block for the platform"""
    new_block = sr.SUB_CONTEXT
    new_block["elements"][0]["text"] = f":pushpin: <https://slack.com/app_redirect?channel={platform.slack_channel}|Join the release channel>."
    
    return new_block
