from configparser import ConfigParser

from loguru import logger

from pprint import pprint as p


class Configuration:
    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read("./config.ini")

    def get_discord_token(self) -> str:
        token = self.parser["info"]["discord_account_token"]
        return token

    def get_log_channel(self) -> int:
        channel_id = self.parser["info"]["logs_channel_id"]
        return channel_id if not 0 else None

    def get_bookmarks(self) -> dict:
        """
        {'emoji': channel_Id}
        """

        bookmark_blocks = [
            x
            for x in self.parser
            if not x.startswith("DEFAULT") and not x.startswith("info")
        ]

        bookmarks = {}
        for block in bookmark_blocks:
            logger.debug(
                f"Obtained emoji {block} with channel id -> {self.parser[block]['channel_id']}"
            )
            bookmarks[block] = int(self.parser[block]["channel_id"])

        return bookmarks
