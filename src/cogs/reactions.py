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

    async def log(self, **kwargs):
        log_channel = self.config.get_log_channel()

        if log_channel is None:
            return

        channel = self.bot.get_channel(log_channel[0])
        await channel.send(log_channel[1].format(**kwargs))

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

        logger.info(
            f"Received reaction {str(payload.emoji)} | {guild.name} | {channel.name} | {message.id}"
        )

        destination = self.bot.get_channel(
            self.bookmarks[str(payload.emoji)]["channel_id"]
        )

        if destination is None:
            raise Exception("Invalid Channel ID provided.")

        attachment_list = []

        if message.attachments:
            logger.info(
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
                emoji=str(payload.emoji),
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
        await self.log(
            author=message.author,
            server=guild,
            message=message,
            time=selfcord.utils.format_dt(message.created_at),
            emoji=str(payload.emoji),
            newline="\n",
        )


async def setup(bot):
    await bot.add_cog(ReactionEvent(bot))
