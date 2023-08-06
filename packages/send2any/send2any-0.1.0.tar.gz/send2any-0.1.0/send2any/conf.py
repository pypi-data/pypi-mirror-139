import logging
import os
from logging import NullHandler


class Config:

    # Services
    DISCORD_EVENTS = os.getenv("DISCORD_EVENTS")
    DISCORD_ERRORS = os.getenv("DISCORD_ERRORS")

    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

    
logging.basicConfig(format="%(asctime)s %(message)s")
logging.getLogger(__name__).addHandler(NullHandler())
