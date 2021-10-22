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

SUB_ACTION_BASE = "edit_subscription_"
SUBSCRIPTION_BUTTON = {
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
				"value": "ROM FAMILY",
				"action_id": "edit_subscription"
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

EDIT_SUB_MODAL = {
	"type": "modal",
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"title": {
		"type": "plain_text",
		"text": "Edit Subscription",
		"emoji": True
	},
	"blocks": [
		{
			"type": "divider"
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": ":x: Unsubscribe",
						"emoji": True
					},
					"value": "unsubscribe",
					"action_id": "unsubscribe",
					"style": "danger"
				}
			]
		}
	]
}

NEW_SUB_MODAL = {
	"title": {
		"type": "plain_text",
		"text": "New Subscription",
		"emoji": True
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit"
	},
	"type": "modal",
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"blocks": [
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":memo: Check all platforms you'd like to subscribe to:"
			},
			"accessory": {
				"type": "checkboxes",
				"options": [
					"PUT CHECKBOXES HERE"
				],
				"action_id": "new_sub_checkbox"
			}
		}
	]
}

NEW_SUB_VALUE_BASE = "new_subscription_"
NEW_SUB_CHECKBOX = {
						"text": {
							"type": "mrkdwn",
							"text": "ROM FAMILY"
						},
						"description": {
							"type": "mrkdwn",
							"text": "DESCRIPTION"
						},
						"value": "NEW SUB VALUE"
					}