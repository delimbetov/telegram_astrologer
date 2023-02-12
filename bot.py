from telethon import TelegramClient, events
from handlers.start import StartHandler
from handlers.text import TextHandler
from logger import get_logger


class BotConfig:
    def __init__(
            self,
            api_id: int,
            api_hash: str,
            token: str,
            openai_api_key: str,
            daily_limit: int):
        if api_id is None:
            raise RuntimeError("Api id must be set")

        if api_hash is None or len(api_hash) < 1:
            raise RuntimeError("Invalid api_hash: " + api_hash)

        if token is None or len(token) < 1:
            raise RuntimeError("Invalid token: " + token)

        if openai_api_key is None or len(openai_api_key) < 1:
            raise RuntimeError("Invalid openai_api_key: " + openai_api_key)

        if daily_limit < 1:
            raise RuntimeError(f"Invalid daily_limit={daily_limit}")

        self.api_id = api_id
        self.api_hash = api_hash
        self.token = token
        self.openai_api_key = openai_api_key
        self.daily_limit = daily_limit

    def __repr__(self):
        return f"App id=***, app hash=***, token=***, path_to_model=***, daily_limit={self.daily_limit}"


class Bot:
    def __init__(self, config: BotConfig):
        if config is None:
            raise RuntimeError("No config passed")

        self.config = config
        get_logger().info(msg="Creating Bot object with config: {}".format(self.config))

        self.client = TelegramClient(
            'astrolog_bot',
            api_id=config.api_id,
            api_hash=config.api_hash).start(bot_token=config.token)

        # Add /start handler
        self.client.add_event_handler(
            callback=StartHandler(),
            event=events.NewMessage(pattern=f'^/(start|help)', incoming=True, outgoing=False))

        # Add text handler
        self.client.add_event_handler(
            callback=TextHandler(openai_api_key=self.config.openai_api_key, daily_limit=self.config.daily_limit),
            event=events.NewMessage(incoming=True, outgoing=False))

    async def arun(self):
        get_logger().info("Awaiting on run_until_disconnected")
        await self.client.run_until_disconnected()

    def run(self):
        get_logger().info("Starting run loop ...")

        with self.client:
            get_logger().info("Starting async run loop ... ")
            self.client.loop.run_until_complete(self.arun())
            get_logger().info("... async run loop is stopped")

        get_logger().info("... run loop is stopped")
