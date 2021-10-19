SUBSCRIPTION_HEADER = {
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Your Subscriptions"
			}
		}

DIVIDER = {
			"type": "divider"
		}

NEW_SUBSCRIPTION_BUTTON = {
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "New Subscription",
						"emoji": True
					},
                    "style": "primary",
					"value": "new_subscription",
					"action_id": "new_subscription"
				}
			]
		}

SUB_ACTION_BASE = "Subscription_"
SUBSCRIPTION = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "ROM FAMILY DESC"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Edit",
					"emoji": True
				},
				"value": "edit_subscription",
				"action_id": "ACTIONID"
			}
		}

SUB_CONTEXT = {
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "CONTEXT"
				}
			]
		}

EMPTY_SUBSCRIPTION = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "You have no subscriptions to any ROM families. Try using the New Subscription button."
			}
		}
