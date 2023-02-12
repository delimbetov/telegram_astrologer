from telethon.events import NewMessage, StopPropagation
from logger import get_logger


class StartHandler:
    def __init__(self):
        pass

    async def __call__(self, event: NewMessage.Event):
        corr_id = f"{event.chat_id}_{event.message.id}"
        get_logger().info(msg=f"corr_id={corr_id}: start or help request: {event.message.message}")

        # send instructions
        await event.message.respond(
            "Hello and welcome! I'm an astrological prediction bot powered by AI. "
            "To receive personalized predictions, simply describe yourself or someone else, "
            "including your/their zodiac sign and what you'd like to know about.\n\n"
            "Here are a couple of example prompts to get you started:\n"
            "⭐️ I'm a Scorpio born on November 1st. I want to know what's in store for me in love this month.\n"
            "⭐️ I want to know what opportunities I'll have in my career as a Taurus in the next 6 months.\n"
            "⭐️ Can you tell me what the next year holds for my financial future as a Gemini?\n\n"
            "Feel free to get creative with your prompts and let's delve into the mysteries of the stars together!\n\n"
            "p.s. You can use any language you're comfortable with, although English is easier for me : )")

        raise StopPropagation
