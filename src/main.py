import os, sys, datetime
from selfcord.ext import commands

from loguru import logger


class ReactionBookmark(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned,
            self_bot=True,
        )

    async def setup_hook(self):
        logger.success(f"Bot has been started up. Welcome {self.user}")

        for filename in os.listdir("./src/cogs"):
            if not filename.startswith("_"):
                logger.success(f"Loaded extension {{cogs.{filename[:-3]}}}")
                await self.load_extension(f"src.cogs.{filename[:-3]}")
