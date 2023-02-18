from telethon.events import NewMessage, StopPropagation
from logger import get_logger
from localization import g_map, g_hello, get_language_from_ietf_code


class SharedHandlerState:
    def __init__(self):
        self.users = dict()

    async def get_language_from_event(self, event: NewMessage.Event) -> tuple:
        chat_id = event.chat_id

        if chat_id not in self.users:
            self.users[chat_id] = dict()

        if "language" not in self.users[chat_id]:
            sender = await event.message.get_sender()
            # language code might be none but its accounted for in function
            language = get_language_from_ietf_code(sender.lang_code)
            get_logger().info(f"Language chosen for chat_id={chat_id}: {language.name}")
            self.users[chat_id]["language"] = language

        return self.users[chat_id]["language"]


class StartHandler:
    def __init__(self, shared_state: SharedHandlerState):
        self.shared_state = shared_state

    async def __call__(self, event: NewMessage.Event):
        corr_id = f"{event.chat_id}_{event.message.id}"
        get_logger().info(msg=f"corr_id={corr_id}: start or help request: {event.message.message}")

        # send instructions
        await event.message.respond(g_map[await self.shared_state.get_language_from_event(event=event)][g_hello])

        raise StopPropagation
