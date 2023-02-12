from bot import Bot, BotConfig
from logger import configure_logging
import sys


def main():
    # Configure logging
    configure_logging(name="astrolog_bot")

    # Parse command line args
    # 0 - prog name
    # 1 - openai api key
    # 2 - api id
    # 3 - api hash
    # 4 - bot token
    # 5 - daily limit
    if len(sys.argv) != 6:
        raise RuntimeError(
            "openai api key, api id, api hash, token, daily limit are required to be passed as command line "
            "argument. sys.argv: {}".format(sys.argv))

    openai_api_key = sys.argv[1]
    api_id = int(sys.argv[2])
    api_hash = sys.argv[3]
    token = sys.argv[4]
    daily_limit = int(sys.argv[5])

    # Load configs
    bot_config = BotConfig(
        api_id=api_id,
        api_hash=api_hash,
        token=token,
        openai_api_key=openai_api_key,
        daily_limit=daily_limit)

    # Create bot obj
    bot = Bot(config=bot_config)

    # Run the bot
    bot.run()


if __name__ == '__main__':
    main()
