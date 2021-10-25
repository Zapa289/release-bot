from abc import ABC, abstractmethod

import lib.slack_repo as sr
from lib.user import User
from lib.platform import Platform

class Action:
    """Slack action class"""
    def __init__(self, action: dict, trigger_id: str, user: User):
        self.action_id: str = action["action_id"]
        self.value: str = action["value"]
        self.block_id:str = action["block_id"]
        self.type: str= action['type']
        self.trigger_id: str = trigger_id
        self.user: User = user

# class Modal(ABC):
#     """Class for modals"""
#     @abstractmethod
#     def create_modal(self, action: Action) -> dict:
#         """Create the modal"""

#     @abstractmethod
#     def get_modal(self) -> dict:
#         """Return the modal"""

# class EditSubscriptionModal(Modal):
#     """Edit Subscription modal"""
#     def __init__(self, action: Action):
#         self.modal = self.create_modal(action)

#     def create_modal(self, action: Action) -> dict:
#         """Create a modal for editing a subscription"""
#         modal = sr.EDIT_SUB_MODAL
#         modal['blocks'][1]['elements'][0]['value'] = action.value

#         return modal

#     def get_modal(self) -> dict:
#         """Return the modal"""
#         return self.modal

# class NewSubscriptionModal(Modal):
#     """Edit Subscription modal"""
#     def __init__(self, action: Action):
#         self.modal = self.create_modal(action)

#     def create_modal(self, action: Action) -> dict:
#         """Create a modal for editing a subscription"""
#         modal = sr.EDIT_SUB_MODAL
#         modal['blocks'][1]['elements'][0]['value'] = action.value

#         return modal

#     def get_modal(self) -> dict:
#         """Return the modal"""
#         return self.modal

    # def get_modal(self) -> Modal:
    #      """Create the proper modal for a given action"""
    #     modal = {}
    #     try:
    #         modal = self.modal_creation_func[self.action_id](self)
    #     except KeyError:
    #         print(f"Unknown action_id: {self.action_id}")

    #     return modal

def create_new_subscription_modal(action: Action, **kwargs) -> dict:
    """Create a modal for picking a new subscription"""

    if 'platforms' not in kwargs.keys():
        print("Platform list missing")
        return {}

    modal = sr.NEW_SUB_MODAL

    new_sub_blocks = []
    for platform in kwargs["platforms"]:
        if platform not in action.user.subscriptions:
            new_sub_blocks.append(make_platform_option(kwargs["platforms"][platform]))

    modal['blocks'][0]['element']["options"] = new_sub_blocks
    print(modal)
    return modal

def make_platform_option(platform: Platform):
    """Make a new option for the new subscription drop down menu"""
    option = sr.NEW_SUB_OPTION
    option['text']['text'] = f"{platform.rom_family} : {platform.description}"
    option['value'] = f"{platform.rom_family}"

    return option

def create_edit_subscription_modal(action: Action, **kwargs) -> dict:
    """Create a modal for editing a subscription"""
    modal = sr.EDIT_SUB_MODAL
    modal['blocks'][1]['elements'][0]['value'] = action.value
    return modal

modal_creation_func = {
        "new_subscription": create_new_subscription_modal,
        "edit_subscription": create_edit_subscription_modal
    }