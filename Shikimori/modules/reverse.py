import requests
import json
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler

from Ishikki import dispatcher


api_key = "blue-api-testing"
url = 'https://blue-api.vercel.app/reverse'

def reverse(update, context):
    message = update.effective_message
    chat_id = update.effective_chat.id

    reply = message.reply_to_message

    if reply:
        if reply.sticker:
            file_id = reply.sticker.file_id
            new_id = reply.sticker.file_unique_id
        elif reply.photo:
            file_id = reply.photo[-1].file_id
            new_id = reply.photo[-1].file_unique_id
        else:
            message.reply_text("Reply To An Image Or Sticker To Lookup!")
            return

        file_path = os.path.join("temp", f"{new_id}.jpg")
        file_obj = context.bot.get_file(file_id)
        file_url = file_obj.file_path
        
    else:
        message.reply_text(
            "Please Reply To A Sticker, Or An Image To Search It!"
        )
        return
    a = message.reply_text("searching...")
    try:
        data = {"img_url": file_url}
        headers = {"API-KEY": api_key}
        try:
            response = requests.post(url, headers=headers, json=data)
            reverse_dict = response.json()
            web_url = reverse_dict["url"]
            textu = reverse_dict["reverse"]
            message.reply_text(
                text=textu,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="Link", url=web_url)
                        ]
                    ]
                )
            )
        except:
            message.reply_text("Cant find anything!!")
    except:
        message.reply_text("Cant find anything!!")
    a.delete()
   

dispatcher.add_handler(CommandHandler(["pp", "grs", "p", "reverse"], reverse))
