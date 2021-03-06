import re
import time
import json
import psutil
from slackclient import SlackClient
import config
import sys

# Prevent python from generating .pyc files.
sys.dont_write_bytecode = True

slack_client = SlackClient(config.api_key_bottington)

user_list = slack_client.api_call("users.list")
for user in user_list.get("members"):
    if user.get("name") == "bottington":
        slack_user_id = user.get("id")
        break

if slack_client.rtm_connect():
    print ("Connected!")

while True:
    for message in slack_client.rtm_read():
        if "text" in message and message ["text"].startswith("<@%s>" % slack_user_id):
            print("Message received: %s" % json.dumps(message, indent = 2))
            message_text = message['text'].\
                    split("<@%s>" % slack_user_id)[1].\
                    strip()

            if re.match(r'.*(cpu).*', message_text, re.IGNORECASE):
                cpu_pct = psutil.cpu_percent(interval = 1, percpu = False)

                slack_client.api_call(
                    "chat.postMessage",
                    channel = message["channel"],
                    text = "My CPU is at %s%%." % cpu_pct,
                    as_user = True)

            if re.match(r'.*(ding).*', message_text, re.IGNORECASE):
                slack_client.api_call(
                    "chat.postMessage",
                    channel = "general",
                    text = "Selecting a winner...",
                    as_user = True)
            else:
                slack_client.api_call(
                    "chat.postMessage",
                    channel = "general",
                    text = "I can only respond to "ding" at this time.",
                    as_user = True)
time.sleep(1)
