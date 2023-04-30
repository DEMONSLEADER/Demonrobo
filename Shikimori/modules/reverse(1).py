# Author: Sasta Dev || https://t.me/SastaDev
# Author's github: https://github.com/SastaDev
# Created on: Saturday, 29 April, 2023.
# Written in python using pyrogram.
# This python script only supports pyrogram versions lower than v2.0.
# © Sasta Dev ~ 2023.

import uuid
from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton, Message)
import httpx

from YourRobot import pbot

API_URL = 'https://sasta.tk/google_reverse'

class STRINGS:
    REPLY_TO_MEDIA = 'Reply to a message having photo, sticker or document.'
    THESE_MEDIA_TYPES_ONLY = 'Only <b>photo</b>, <b>sticker</b> and <b>document</b> media types are allowed.'
    GIF_NOT_SUPPORTED = 'GIF reverse is currently not available.'
    DOWNLOADING_MEDIA = '<b>• Downloading media...</b>'
    UPLOADING_MEDIA = '<b>• Uploading media...</b>'
    API_ERROR = '<b>An API Error occured while requesting:</b>:\n{}'
    SUPPORT_CHAT = '<b>Support Chat:</b> @HelpSupportChat'
    REVERSE_RESULT = '''
<b>Search Keyword:</b> <code>{}</code>
<b>Results link:</b> <a href='{}'>Link</a>.

<b>Credits:</b> @SastaDev
    '''

COMMANDS = ['reverse', 'grs', 'pp']

@pbot.on_message(filters.command(COMMANDS))
async def on_reverse(client: Client, message: Message) -> Message:
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply(STRINGS.REPLY_TO_MEDIA)
        return
    media_type = message.reply_to_message.media
    if media_type not in ('photo', 'sticker', 'document'):
        if media_type == 'animation':
            await message.reply(STRINGS.GIF_NOT_SUPPORTED)
            return
        await message.reply(STRINGS.THESE_MEDIA_TYPES_ONLY)
        return
    status_msg = await message.reply(STRINGS.DOWNLOADING_MEDIA)
    file_path = f'downloads/{uuid.uuid4()}'
    await message.reply_to_message.download(file_path)
    await status_msg.edit(STRINGS.UPLOADING_MEDIA)
    async with httpx.AsyncClient(timeout=30) as async_client:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = await async_client.post(API_URL, files=files)
        response_json = response.json()
        if response.status_code != 200:
            await message.reply(STRINGS.API_ERROR.format(response_json['error']) + STRINGS.SUPPORT_CHAT)
            return
        search_keyword = response_json['keyword']
        url = response_json['url']
    text = STRINGS.REVERSE_RESULT.format(search_keyword, url)
    reply_markup = [
        [InlineKeyboardButton('Open Link', url=url)]
        ]
    await message.reply(text, reply_markup=InlineKeyboardMarkup(reply_markup))
    await status_msg.delete()