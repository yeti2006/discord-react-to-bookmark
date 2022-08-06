from src.main import ReactionBookmark
from src.utils.config import Configuration

from loguru import logger
import sys

config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<c>{time:hh:mm:ss}</c> | <green><bold>{level}</bold></green> | <red>{name}:{function}</red> - <y>{message}</y>",
        },
    ]
}

logger.configure(**config)

bot = ReactionBookmark().run(Configuration().get_discord_token())
