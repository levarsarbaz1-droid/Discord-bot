import discord
import requests

# Paste your Bot Token inside the quotes
BOT_TOKEN = "MTU2NTc1NDM4NzAxODU0NzM4MA.GvErEB.6gKThi9WMp8yoW3ZburqbKljtfWYwHfaYinj3g"

# Paste your Webhook URL inside the quotes
WEBHOOK_URL = "https://discord.com/api/webhooks/1565755991482437705/WEpMnwQs1APUuQsxtnbN1xihFaMW3Jk7Fsn8Qy3nUi8iOBgYmJVVG7Lj8hqn3qTmWFc5"

# Put your target channel ID here (e.g., [123456789012345678]), or leave [] to log ALL channels
MONITORED_CHANNEL_IDS = [] 

intents = discord.Intents.default()
intents.message_content = True  # Needed to read message text

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} - Logger is active!')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself or webhooks
    if message.author.bot or message.webhook_id:
        return

    # Filter by specific channels if specified
    if MONITORED_CHANNEL_IDS and message.channel.id not in MONITORED_CHANNEL_IDS:
        return

    # Check for image/video attachments
    attachment_urls = [att.url for att in message.attachments]
    attachment_text = "\n**Attachments:**\n" + "\n".join(attachment_urls) if attachment_urls else ""

    # Send message details to your webhook log channel
    payload = {
        "username": f"Log: {message.author.name}",
        "avatar_url": str(message.author.display_avatar.url),
        "content": f"**[#{message.channel.name}]** {message.content}{attachment_text}"
    }

    requests.post(WEBHOOK_URL, json=payload)

client.run(BOT_TOKEN)