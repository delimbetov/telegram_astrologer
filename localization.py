from enum import Enum
from logger import get_logger

g_map = dict()

# handlers
g_hello = "hello"

# text
g_text_new_prompt = "text_new_prompt"
g_text_daily_limit_0 = "text_daily_limit_0"
g_text_daily_limit_1 = "text_daily_limit_1"


class Language(Enum):
    RUSSIAN = 0
    ENGLISH = 1

    def get_property_file_suffix(self):
        if self == Language.RUSSIAN:
            return "ru"
        elif self == Language.ENGLISH:
            return "en"

        raise RuntimeError("Unsupported language")


# English
g_map[Language.ENGLISH] = {
    g_hello: """🌟 Hello and welcome! I'm an astrological prediction bot powered by OpenAI. To receive personalized predictions, simply describe yourself or someone else, including your/their zodiac sign and what you'd like to know about. You can use any language that you're comfortable with! 🌎 Please note that while I can process prompts in any language, the quality of my responses may be highest when you use English. 📈 Let's explore your astrological future together!

Here are a couple of example prompts to get you started:

"I'm a Scorpio born on November 1st. I want to know what's in store for me in love this month."
"I want to know what opportunities I'll have in my career as a Taurus in the next 6 months."
"Can you tell me what the next year holds for my financial future as a Gemini?"
Feel free to get creative with your prompts and let's delve into the mysteries of the stars together! 🔮""",
    g_text_new_prompt: "I'm sorry, I didn't quite understand what you're looking for. "
                       "Could you please provide a proper astrological prompt, "
                       "including your zodiac sign and the information you'd like to know about?\n"
                       "Use /help to see example prompts.",
    g_text_daily_limit_0: "I do have a daily limit on the number of predictions (",
    g_text_daily_limit_1: ") I can provide for each "
                          "user. This is to ensure that I can keep providing high-quality astrological insights to everyone "
                          "while also taking care of my AI self."
}

# Russian
g_map[Language.RUSSIAN] = {
    g_hello: """🌟 Здравствуйте и добро пожаловать! Я бот для астрологических предсказаний, работающий на базе OpenAI. Чтобы получить персональные прогнозы, достаточно просто описать себя или другого человека, указав знак зодиака и то, что вас интересует. Можете использовать любой язык, который вам удобен! 🌎 Обратите внимание, что хоть я могу обрабатывать запросы на любом языке, лучшее качество ответов будет на английском языке. 📈 Давайте вместе исследуем ваше астрологическое будущее!

Вот несколько примеров запросов, чтобы вы смогли начать:

«Я Скорпион, родился 1 ноября. Хочу знать, что меня ждет в любви в этом месяце».
«Я хочу узнать, какие возможности у меня будут в карьере в ближайшие 6 месяцев, я Телец».
«Можете рассказать мне, что ждет мой финансовый будущее, если я Рак, в следующем году?»
Обращайтесь с любыми вопросами и давайте вместе исследовать тайны звезд! 🔮""",
    g_text_new_prompt: """Простите, я не до конца понял, что вы ищете. Можете, пожалуйста, сформулировать астрологический запрос, уточнив ваш знак зодиака и то, что вас интересует?
Если вам нужны примеры запросов, используйте команду /help.""",
    g_text_daily_limit_0: "У меня есть ограничение на количество предсказаний - ",
    g_text_daily_limit_1: " для каждого пользователя в день. Это необходимо, чтобы я мог продолжать предоставлять высококачественные астрологические прогнозы каждому пользователю, одновременно заботясь о своём AI-сердце."
}

g_ietf_russian = "ru"
g_ietf_english = "en"


def get_language_from_ietf_code(ietf_language_code: str) -> Language:
    lang_code = str()

    if ietf_language_code is None:
        lang_code = g_ietf_english
        get_logger().warning(f"ietf language code is None; defaulted to {lang_code}")
    else:
        lang_code = ietf_language_code

    lowered = lang_code.lower()

    if lowered == g_ietf_russian:
        return Language.RUSSIAN
    elif lowered.startswith(g_ietf_english):
        return Language.ENGLISH

    # default to english
    get_logger().warning(f"Unknown language code={ietf_language_code}. Default to ENGLISH")
    return Language.ENGLISH
