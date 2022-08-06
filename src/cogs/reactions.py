import selfcord
from selfcord.ext import commands

from io import BytesIO
from loguru import logger

from ..utils.config import Configuration


class ReactionEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = Configuration()
        self.bookmarks = self.config.get_bookmarks()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: selfcord.RawReactionActionEvent):
        if (
            not payload.member.id == self.bot.user.id
            or not str(payload.emoji) in self.bookmarks
        ):
            return

        guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        logger.debug(
            f"Received reaction {str(payload.emoji)} | {guild.name} | {channel.name} | {message.id}"
        )

        destination = self.bot.get_channel(
            self.bookmarks[str(payload.emoji)]["channel_id"]
        )

        if destination is None:
            raise Exception("Invalid Channel ID provided.")

        attachment_list = []

        if message.attachments:
            logger.debug(
                "Attachments found: "
                + ", ".join([x.filename for x in message.attachments])
            )

            for attachment in message.attachments:
                bytes = await attachment.read()
                attachment_list.append((bytes, attachment.filename))

        await destination.send(
            self.bookmarks[str(payload.emoji)]["message_format"].format(
                author=message.author,
                server=guild,
                message=message,
                time=selfcord.utils.format_dt(message.created_at),
                newline="\n",
            ),
            files=[
                selfcord.File(BytesIO(attachment[0]), filename=attachment[1])
                for attachment in attachment_list
            ]
            if attachment_list
            else None,
        )

        logger.success(f"Succesfully sent to: #{destination} | {destination.guild}")


async def setup(bot):
    await bot.add_cog(ReactionEvent(bot))
