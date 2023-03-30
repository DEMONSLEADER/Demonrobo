from pyrogram import filters
from Shikimori import pbot as app
from pyrogram.types import Message
from telegraph import upload_file
import requests
import time

# Bot code
@app.on_message(filters.command("wanted") & filters.group)
async def upload_pfp(_, message: Message):
    a = await message.reply("**Processing...**")
               

    try:
        photo = None
        fname = None
        if message.reply_to_message:
            if message.reply_to_message.from_user.photo:
                photo = await app.download_media(
                    message.reply_to_message.from_user.photo.big_file_id
                )
                fname = message.reply_to_message.from_user.first_name
        else:
            fname = message.from_user.first_name
            if message.from_user.photo:
                photo = await app.download_media(message.from_user.photo.big_file_id)

        if photo:
            try:
                media_urls = upload_file(photo)
                media_url = "https://telegra.ph" + media_urls[0]
            except Exception as e:
                raise Exception(f"Failed to upload image: {e}")
            response = requests.post(
                "https://bounty.some-1hing.repl.co/wanted",
                json={
                    "fname": fname,
                    "img": media_url,
                },
            )

            if response.status_code == 200:
                response_json = response.json()
                img_url = response_json.get("img")
                await message.reply_photo(img_url)
                
               
            else:
                raise Exception(f"API request failed: {response.json().get('message')}")
        else:
            await message.reply("Please upload a photo to use this command.")
    except Exception as e:
        await message.reply(f"Sorry, something went wrong. Error message: {e}")
    a.delete()
    time.sleep(2)
