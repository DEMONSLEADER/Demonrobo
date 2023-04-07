'''
This Project Is Created By @ImmortalsXKing
'''
import requests
from pyrogram import *
from pyrogram.types import *
from pyrogram.enums import *
from Shikimori import pbot

@pbot.on_message(filters.command("cosplay"))
async def waifu(_,message: Message):
  if message.chat.type != ChatType.PRIVATE:    
    r = requests.get("https://waifu-api.vercel.app").json() #api credit- @YASH_SHARMA_1807 on telegram
    await message.reply_photo(r)
  else:
    await message.reply("**Use This Command In Group**")
    
@pbot.on_message(filters.command("ncosplay"))
async def waifus(_,message: Message):
  if message.chat.type == ChatType.PRIVATE:    
    rape = requests.get("https://waifu-api.vercel.app/items/1").json()
    await message.reply_photo(rape)
  else:
    await message.reply("**Use This Command In PM**")
    
