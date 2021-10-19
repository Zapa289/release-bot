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

SUBSCRIPTION = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*#public-relations*\n<fakelink.toUrl.com|PR Strategy 2019> posts new tasks, comments, and project updates to <fakelink.toChannel.com|#public-relations>"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Edit",
					"emoji": True
				},
				"value": "edit_subscription",
				"action_id": "edit_subscription"
			}
		}

EMPTY_SUBSCRIPTION = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "You have no subscriptions to any ROM families. Try using the New Subscription button."
			}
		}
