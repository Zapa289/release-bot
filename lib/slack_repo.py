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
						"text": "Unsubscribe",
						"emoji": True
					},
					"value": "ROM FAMILY",
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
			"type": "input",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "PUT OPTIONS HERE",
							"emoji": True
						},
						"value": "value-0"
					}
				],
				"action_id": "static_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": ":memo: Select a platform you'd like to subscribe to:",
				"emoji": True
			}
		}
	]
}

NEW_SUB_OPTION = {
					"text": {
						"type": "plain_text",
						"text": "ROM FAMILY : DESCRIPTION",
						"emoji": True
					},
					"value": "ROM FAMILY"
				}