#CREATED BY @O_okarma
#PROVIDED BY @NovaXMod


#IMPORTS 
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

#REPO => Your Bots File Name
import Shikimori.modules.sql.users_sql as sql
from Shikimori import DEV_USERS, OWNER_ID, pbot as pgram
from Shikimori.modules.sql.users_sql import get_all_users

#Broadcast Function
@pgram.on_message(filters.command("broadcast"))
async def broadcast_cmd(client: Client, message: Message):
    user_id = message.from_user.id
    texttt = message.text.split(" ")

    if user_id not in [OWNER_ID] + DEV_USERS:
        await message.reply_text(
            "You are not authorized to use this command. Only the owner and authorized users can use it."
        )
        return

    if len(texttt) < 2:
        return await message.reply_text(
            "<b>BROADCASTING COMMANDS</b>\n-user : broadcasting all user's DM\n-group : broadcasting all groups\n-all : broadcasting both\nEx: /broadcast-user"
        )

    if message.reply_to_message is None and not get_arg(message):
        return await message.reply_text(
            "<b>Please provide a message or reply to a message</b>"
        )

    tex = await message.reply_text("<code>Starting global broadcast...</code>")

    usersss = 0
    chatttt = 0
    uerror = 0
    cerror = 0
    chats = sql.get_all_chats() or []
    users = get_all_users()

    if "-all" in texttt:
        texttt.append("-user")
        texttt.append("-group")

    if "-user" in texttt:
        for chat in users:
            if message.reply_to_message:
                msg = message.reply_to_message
            else:
                msg = get_arg(message)
            try:
                if message.reply_to_message:
                    aa = await msg.copy(chat.user_id)
                else:
                    aa = await client.send_message(chat.user_id, msg)

                usersss += 1
                await asyncio.sleep(0.3)
            except Exception:
                uerror += 1
                await asyncio.sleep(0.3)
    if "-group" in texttt:
        for chat in chats:
            if message.reply_to_message:
                msg = message.reply_to_message
            else:
                msg = get_arg(message)
            try:
                if message.reply_to_message:
                    aa = await msg.copy(chat.chat_id)
                else:
                    aa = await client.send_message(chat.chat_id, msg)

                chatttt += 1
                await asyncio.sleep(0.3)
            except Exception:
                cerror += 1
                await asyncio.sleep(0.3)

    await tex.edit_text(
        f"<b>Message Successfully Sent</b> \nTotal Users: <code>{usersss}</code> \nFailed Users: <code>{uerror}</code> \nTotal GroupChats: <code>{chatttt}</code> \nFailed GroupChats: <code>{cerror}</code>"
    )
