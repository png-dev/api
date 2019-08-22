import os
from slackclient import SlackClient


SLACK_TOKEN = os.environ.get('SLACK_TOKEN', 'xoxp-170449210610-184880281927-369424300784-89961d12a3894b7c44c0c596218ce68b')

slack_client = SlackClient(SLACK_TOKEN)


def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call['ok']:
        return channels_call['channels']
    return None


def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='pythonbot',
        icon_emoji=':robot_face:'
    )


def notify_message(message):
    channels = list_channels()
    if channels:
        for channel in channels:
            if channel['name'] == 'api':
                send_message(channel['id'], message)
                break
