import json
import lib.slack_repo as sr
from lib.user import User
from db_manager import DatabaseAccess

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
    sub_blocks = list

    for platform in user.subscriptions:
        db.get_platform(platform)
        new_block = dict
        sub_blocks.append(new_block)

    return sub_blocks