from configparser import ConfigParser
from loguru import logger
import os

DEFAULT_MESSAGE_FORMAT = "**{author}**(_{server}_) - {time}{newline}{message.content}"


class Configuration:
    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read("./config.ini")

    def get_discord_token(self) -> str:
        token = str(self.parser["info"]["discord_account_token"])
        if "your_account_token" in token:
            token = os.environ.get("discord_account_token")

        return str(token)

    def get_log_channel(self) -> int:
        channel_id = int(self.parser["info"]["logs_channel_id"])
        message_format = str(self.parser["info"]["message_format"])

        return (
            (channel_id, message_format if message_format else DEFAULT_MESSAGE_FORMAT)
            if not channel_id == 0
            else None
        )

    def get_bookmarks(self) -> dict:
        """
        {'emoji': {'channel_id': 123, 'message_format': 'abc'}}
        """

        bookmark_blocks = [
            x
            for x in self.parser
            if not x.startswith("DEFAULT") and not x.startswith("info")
        ]

        bookmarks = {}
        for block in bookmark_blocks:
            logger.info(
                f"Obtained emoji {block} with channel id -> {self.parser[block]['channel_id']}"
            )
            message_format = str(self.parser[block]["message_format"])

            bookmarks[block] = {
                "channel_id": int(self.parser[block]["channel_id"]),
                "message_format": message_format
                if message_format
                else DEFAULT_MESSAGE_FORMAT,
            }

        return bookmarks
