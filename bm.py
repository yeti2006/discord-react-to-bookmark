from src.main import ReactionBookmark
from src.utils.config import Configuration

bot = ReactionBookmark().run(Configuration().get_discord_token())
