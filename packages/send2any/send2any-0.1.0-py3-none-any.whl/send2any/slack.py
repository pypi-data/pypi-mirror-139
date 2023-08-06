import httpx

from send2any.conf import Config

SLACK_API = "https://slack.com/api/"


class SlackCient:

    def __init__(self, tkn=Config.SLACK_BOT_TOKEN):
        self._headers = {"Authorization": f"Bearer {tkn}"}

    def list_channels(self):
        r = httpx.get(f"{SLACK_API}/conversations.list",
                      headers=self._headers)
        return r.json()

    def send(self, channel, text):
        r = httpx.post(f"{SLACK_API}/chat.postMessage",
                       headers=self._headers,
                       data=dict(channel=channel, text=text)
                       )
        return r.json()
