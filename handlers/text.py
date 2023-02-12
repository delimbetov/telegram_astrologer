from telethon.events import NewMessage, StopPropagation
from logger import get_logger
from datetime import date
import openai


async def complete(corr_id, model, prompt, temperature, max_tokens):
    get_logger().info(msg=f"corr_id={corr_id}: requesting completion with args: model={model},"
                          f"prompt={prompt}, temp={temperature}, max_tokens={max_tokens}")
    response = await openai.Completion.acreate(model=model, prompt=prompt, temperature=temperature,
                                               max_tokens=max_tokens)

    get_logger().info(msg=f"corr_id={corr_id}: response={response}")
    return response


async def ask_for_new_prompt(event: NewMessage.Event):
    await event.message.respond(
        "I'm sorry, I didn't quite understand what you're looking for. "
        "Could you please provide a proper astrological prompt, "
        "including your zodiac sign and the information you'd like to know about?\n"
        "Use /help to see example prompts.")


class TextHandler:
    def __init__(self, openai_api_key, daily_limit):
        self.counters = dict()
        self.daily_limit = daily_limit
        self.last_write_date = date.today()

        openai.api_key = openai_api_key

    async def __call__(self, event: NewMessage.Event):
        corr_id = f"{event.chat_id}_{event.message.id}"

        # reset rate limit counters if its next day already
        if self.last_write_date < date.today():
            get_logger().info(msg=f"Reset counters since date changed from {self.last_write_date} to {date.today()}")
            self.last_write_date = date.today()
            self.counters = dict()

        # rate limit
        if event.chat_id not in self.counters:
            self.counters[event.chat_id] = 0

        count = self.counters[event.chat_id]
        get_logger().info(
            msg=f"corr_id={corr_id}: text handler called; count={count}; text={event.message.message}")

        if count >= self.daily_limit:
            await event.message.respond(
                f"I do have a daily limit on the number of predictions ({self.daily_limit}) I can provide for each "
                f"user. This is to ensure that I can keep providing high-quality astrological insights to everyone "
                f"while also taking care of my AI self.")
            get_logger().info(msg=f"corr_id={corr_id}: count={count}. Count of predictions is over the limit")
            raise StopPropagation

        self.counters[event.chat_id] += 1

        # estimate if prompt is reasonable
        estimate_prompt = "You are Astrologer. " \
                          "You are given a prompt from someone who wants to get astrological prediction. " \
                          "You need to estimate whether that prompt is reasonable to ask an Astrologer. " \
                          "You need to give it a score (integer between 0 and 10). The higher the score, the " \
                          "more likely it is that it the prompt makes sense to do prediction on. " \
                          "Assume that anything less than 5 is probably not something one should ask Astrologer. \n" \
                          f"User's prompt: \"{event.message.message}\".\n" \
                          f"Your output should only be a single score number."

        estimate_response = await complete(corr_id=corr_id, model="text-davinci-003", prompt=estimate_prompt,
                                           temperature=0.6,
                                           max_tokens=24)

        # # parse output
        try:
            score = int(estimate_response.choices[0].text)
        except Exception as e:
            get_logger().error(msg=f"corr_id={corr_id}: Model's score is not castable to int: {e}")
            await ask_for_new_prompt(event=event)
            raise StopPropagation

        if score < 5:
            get_logger().info(msg=f"corr_id={corr_id}: Model's score {score} < 5")
            await ask_for_new_prompt(event=event)
            raise StopPropagation

        # do prediction
        today_date_str = date.today().strftime("%A, %d of %B, %Y")
        prompt = f"Today is {today_date_str}. You are Astrologer. You do typical astrological predictions " \
                 "about future based on user's prompt.\n" + \
                 "You try to use as much info from the prompt as possible to make it feel personalized.\n" \
                 "Add appropriate emojis. Don't make the prediction too positive, be neutral, so it's is " \
                 "interesting for the user. \n" \
                 "You always answer in the same language User used. Try to produce 2 paragraphs of text.\n" \
                 f"User's prompt: \"{event.message.message}\"."
        response = await complete(corr_id=corr_id, model="text-davinci-003", prompt=prompt,
                                  temperature=0.6,
                                  max_tokens=1024)

        # # parse output
        try:
            prediction = str(response.choices[0].text)
        except Exception as e:
            get_logger().error(msg=f"Model's prediction is not a string: {e}")
            await ask_for_new_prompt(event=event)
            raise StopPropagation

        if len(prediction) < 10:
            get_logger().error(msg=f"Model's prediction is too short: {len(prediction)}")
            await ask_for_new_prompt(event=event)
            raise StopPropagation

        # Send prediction to user
        await event.message.respond(prediction)

        raise StopPropagation
