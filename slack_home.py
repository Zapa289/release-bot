import json
from lib.platform import Platform
import lib.slack_repo as sr
from lib.user import User

def get_home_tab(user: User, platform_info: dict[str, Platform]) -> str:
    """Generate the Hope tab for a user"""

    sub_blocks: list = get_subscription_blocks(user, platform_info)

    if not sub_blocks:
        sub_blocks = sr.EMPTY_SUBSCRIPTION

    home_tab = {
        "type": "home",
        "blocks": [sr.SUBSCRIPTION_HEADER,
                sr.NEW_SUBSCRIPTION_BUTTON,
                sr.DIVIDER
                ]
        }

    home_tab["blocks"] = home_tab["blocks"] + sub_blocks
    return json.dumps(home_tab)

def get_subscription_blocks(user: User, platform_info: dict[str, Platform]) -> list:
    """Get all the slack blocks for different """
    sub_blocks: list[dict] = []

    for platform in user.subscriptions:
        try:
            platform_info = platform_info[platform]
        except KeyError:
            #Need to log
            continue
            #raise PlatformNotFound(message=f"Platform '{platform}' could not be found.")

        sub_blocks.append(new_subscription_block(platform_info))
        sub_blocks.append(new_context_block(platform_info))
        sub_blocks.append(sr.DIVIDER)

    return sub_blocks

def new_subscription_block(platform: Platform) -> dict:
    """Create a new subscription block cooresponding to the platform"""
    new_block = sr.SUBSCRIPTION_BUTTON
    new_block["text"]["text"] = f"*{platform.rom_family} ROM*\n{platform.description}"
    new_block["accessory"]["value"] = platform.rom_family

    return new_block

def new_context_block(platform: Platform) -> dict:
    """Create a new helper text block for the platform"""
    new_block = sr.SUB_CONTEXT
    if not platform.slack_channel:
        new_block["elements"][0]["text"] = f":warning: There is currently no available release channel for the {platform.rom_family} ROM."
    else:
        new_block["elements"][0]["text"] = f":pushpin: Join the <https://slack.com/app_redirect?channel={platform.slack_channel}|release channel>."

    return new_block

#
# Modals
#


