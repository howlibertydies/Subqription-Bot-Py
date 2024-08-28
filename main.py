import discord
import requests
from discord.ext import tasks

TOKEN = "replace with your own token"
CHANNEL_ID = int("1255263173968265237")
MESSAGE_ID = int("1277530682897334364")
YOUTUBE_CHANNEL_ID = "replace with your own youtube channel id"
YOUTUBE_API_KEY = "replace with your own api key"

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot is ready")
    await update_subscriber_count.start()

@tasks.loop(minutes=30)
async def update_subscriber_count():
    try:
        channel = client.get_channel(CHANNEL_ID)
        if channel is None:
            print(f"Channel with ID {CHANNEL_ID} not found.")
            return

        url = f"https://www.googleapis.com/youtube/v3/channels"
        params = {
            'part': 'statistics',
            'id': YOUTUBE_CHANNEL_ID,
            'key': YOUTUBE_API_KEY,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        subscriber_count = data['items'][0]['statistics']['subscriberCount']
        message_content = f"Prediqtt subscriber count is currently at **{subscriber_count}** subscribers on YouTube!"

        message = await channel.fetch_message(MESSAGE_ID)
        await message.edit(content=message_content)
        print("Message edited successfully")
    except Exception as e:
        print(f"Failure in updating subscriber count or editing the message: {e}")

client.run(TOKEN)
