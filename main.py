import httpx
import interactions

DISCORD_TOKEN = "discord-token"
DISCORD_DEFAULT_SCOPE = 1234

API_KEYS = ["api-key-0",
            "api-key-1"]
LAST_KEY = API_KEYS[0]


def api_key_selector():
    """
    Choose API key by last used key. If key 0 is used last time use key 1 and vice versa.

    Returns:
        str: API Key
    """
    global LAST_KEY

    if len(API_KEYS) == 2:
        if LAST_KEY == API_KEYS[0]:
            LAST_KEY = API_KEYS[1]
            print("Used API_KEY[1].")
            return API_KEYS[1]

        if LAST_KEY == API_KEYS[1]:
            LAST_KEY = API_KEYS[0]
            print("Used API_KEY[0].")
            return API_KEYS[0]
    else:
        return API_KEYS[0]


bot = interactions.Client(token=DISCORD_TOKEN, default_scope=DISCORD_DEFAULT_SCOPE)


@bot.event
async def on_ready():
    """
    When the bot is ready print some information about it.
    """
    print(f"We have logged in as {bot.me.name}.")
    print(f"Latency: {round(bot.latency)}ms.")


@bot.command(
    name="ask",
    description="Ask anything to OpenAI!",
    options=[
        interactions.Option(
            type=interactions.OptionType.STRING,
            name="question",
            description="What you want to ask?",
            required=True,
        ),
    ],
)
async def ask(ctx: interactions.CommandContext, question: str):
    """
    Let's you ask anything to OpenAI.

    Args:
        ctx (interactions.CommandContext): Context of slash command
        question (str): User input after /ask command
    """
    url = "https://api.openai.com/v1/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key_selector()}'}
    data = {
        "model": "text-davinci-002",
        "prompt": f"{question}",
        "max_tokens": 55,
        "temperature": 1,
    }
    response = httpx.post(url, json=data, headers=headers)
    response_text = response.json()['choices'][0]['text']

    await ctx.send(f"{response_text}")

bot.start()
