from lib import Action, slack_client, modal_creation_func, User, UserNotFound
import slack_home as home
from db_manager import DatabaseAccess

class ReleaseBot:
    """Release bot functions"""
    def __init__(self, db: DatabaseAccess):
        self.db = db
        self.process_event_func = {
            'block_actions' : self.process_block_action,
            'view_submission' : self.process_view_submission
        }

    def process_block_action(self, event):
        """Process a user action"""
        #check what action prompted the event
        action_event = event["actions"][0]
        trigger_id = event['trigger_id']
        user_id = event['user']

        action = Action(action_event, trigger_id)

        #create proper modal
        try:
            modal = modal_creation_func[action.action_id](action, platforms=self.db.platforms)
        except KeyError:
            print(f"Unknown action_id: {action.action_id}")
            return

        #send up the modal
        if modal:
            slack_client.open_modal(action.trigger_id, modal)

    def process_view_submission(self, event):
        """Process a view submission"""
        pass

    def get_home_tab(self, event) -> dict:
        """Get the home tab for a user"""
        home_blocks = {}
        user_id = event.get('user')
        user = self.create_user(user_id)
        if not user:
            raise UserNotFound(user_id=user_id)

        home_blocks = home.get_home_tab(user, self.db.platforms)

        return home_blocks

    def create_user(self, slack_id: str) -> User:
        """Create a new User object."""
        try:
            user: User = slack_client.new_slack_user(slack_id)
        except UserNotFound:
            return None

        user.is_admin = user.id in self.db.admin_ids
        user.owned_platforms =  self.db.get_owner_platforms(user.id)
        user.subscriptions = self.db.get_user_subscriptions(user.id)

        return user

    def process_event(self, event) -> str:
        """Process slack event"""
        response = ""

        event_type = event["type"]
        response = self.process_event_func[event_type](event)

        return response
