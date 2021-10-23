from abc import ABC, abstractmethod
import lib.slack_repo as sr

class Modal(ABC):
    """Class for modals"""
    @abstractmethod
    def create_modal(action: dict) -> dict:
        """Create the modal"""

class EditSubscriptionModal(Modal):
    """Edit Subscription modal"""
    def __init__(self, action):
        self.action = action

    def create_modal() -> dict:
        """Create a modal for editing a subscription"""
        modal = sr.EDIT_SUB_MODAL
        modal['blocks'][1]['elements'][0]['value'] = self.value

        return modal

class Action:
    """Slack action class"""
    def __init__(self, action: dict, trigger_id: str):
        self.action_id: str = action["action_id"]
        self.value: str = action["value"]
        self.block_id:str = action["block_id"]
        self.type: str= action['type']
        self.trigger_id: str = trigger_id

    def get_modal(self) -> Modal:
         """Create the proper modal for a given action"""
        modal = {}
        try:
            modal = self.modal_creation_func[self.action_id]()
        except KeyError:
            print(f"Unknown action_id: {self.action_id}")

        return modal

    # def get_modal(self) -> dict:
    #     """Create the proper modal for a given action"""
    #     modal = {}
    #     try:
    #         modal = self.modal_creation_func[self.action_id]()
    #     except KeyError:
    #         print(f"Unknown action_id: {self.action_id}")

    #     return modal

    def create_new_subscription_modal(self) -> dict:
        """Create a modal for picking a new subscription"""
        modal = sr.NEW_SUB_MODAL

        return modal

    def create_edit_subscription_modal(self) -> dict:
        """Create a modal for editing a subscription"""
        modal = sr.EDIT_SUB_MODAL
        modal['blocks'][1]['elements'][0]['value'] = self.value
        return modal

    modal_creation_func = {
        "new_subscription": create_new_subscription_modal,
        "edit_subscription": EditSubscriptionModal
    }