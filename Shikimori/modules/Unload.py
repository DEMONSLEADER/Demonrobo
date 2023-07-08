#credit to bot


import requests
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ChatType
from Shikimori import pbot

# Define your Telegram bot API token
api_token = "YOUR_TELEGRAM_BOT_API_TOKEN"

# Create a Pyrogram client
client = Client("my_bot", api_id=12345, api_hash="YOUR_API_HASH", bot_token=api_token)

# Define a command to unload the module
@client.on_message(filters.command("unload"))
def unload_module(client: Client, message: Message):
    # Check if the message is from a private chat
    if message.chat.type == ChatType.PRIVATE:
        # Get the module name from the command arguments
        module_name = message.text.split(" ", 1)[1]
        
        # Unload the module using the pbot unload_module function
        pbot.unload_module(module_name)
        
        # Send a response message
        client.send_message(message.chat.id, f"Module {module_name} unloaded successfully!")
    else:
        # Respond with an error message if the command is used in a group chat
        client.send_message(message.chat.id, "This command can only be used in a private chat.")

# Start the bot
client.start()
client.run()
￼Enter
