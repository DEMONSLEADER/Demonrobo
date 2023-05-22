
import time
import re
from Shikimori.__main__ import HELPABLE, IMPORTED, USER_SETTINGS, CHAT_SETTINGS
from Shikimori.modules.helper_funcs.readable_time import get_readable_time
from Shikimori import (
    BOT_USERNAME,
    UPDATE_CHANNEL,
    SUPPORT_CHAT,
    dispatcher,
    StartTime
)
from Shikimori.modules.helper_funcs.misc import paginate_modules
from Shikimori.modules.helper_funcs.chat_status import is_user_admin
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import escape_markdown

bot_name = f"{dispatcher.bot.first_name}"
START_MEDIA = "https://telegra.ph/file/98bee495cac6bd0a9f9e1.jpg"
IMG_START = START_MEDIA.split(".")
start_id = IMG_START[-1]

PM_START_TEXT = f"""
𝙸'𝚖 {bot_name} 𝙺𝚊𝚐𝚞𝚢𝚊 𝚂𝚊𝚖𝚊 𝙻𝚘𝚟𝚎 𝙸𝚜 𝚆𝚊𝚛 𝚋𝚊𝚜𝚎𝚍 𝚐𝚛𝚘𝚞𝚙 𝚖𝚊𝚗𝚊𝚐𝚎𝚖𝚎𝚗𝚝 𝚋𝚘𝚝.
➖➖➖➖➖➖➖➖➖➖➖➖➖
♡ 𝙸 𝚙𝚛𝚘𝚖𝚒𝚜𝚎 𝚝𝚘 𝚙𝚛𝚘𝚝𝚎𝚌𝚝 𝚢𝚘𝚞𝚛 𝚐𝚛𝚘𝚞𝚙 𝚊𝚝 𝚊𝚕𝚕 𝚌𝚘𝚜𝚝𝚜
➖➖➖➖➖➖➖➖➖➖➖➖➖
𝙲𝚑𝚎𝚌𝚔𝚘𝚞𝚝 𝚖𝚢 𝚌𝚘𝚖𝚖𝚊𝚗𝚍𝚜 𝚋𝚢 𝚌𝚕𝚒𝚌𝚔𝚒𝚗𝚐 𝚋𝚎𝚕𝚘𝚠 𝚋𝚞𝚝𝚝𝚘𝚗𝚜.××
"""

HELP_STRINGS = """
ℂ𝕝𝕚𝕔𝕜 𝕠𝕟 𝕥𝕙𝕖 𝕓𝕦𝕥𝕥𝕠𝕟 𝕓𝕖𝕝𝕠𝕨 𝕥𝕠 𝕘𝕖𝕥 𝕕𝕖𝕤𝕔𝕣𝕚𝕡𝕥𝕚𝕠𝕟 𝕒𝕓𝕠𝕦𝕥 𝕞𝕪 𝕤𝕡𝕖𝕔𝕚𝕗𝕚𝕔 𝕗𝕖𝕒𝕥𝕦𝕣𝕖𝕤."""

buttons = [
    [
        InlineKeyboardButton(
            text=f" Add {bot_name} to your Group", url=f"t.me/Chikaxprobot?startgroup=true"),
    ],
    [
        InlineKeyboardButton(text=" 💘𝔸𝕓𝕠𝕦𝕥", callback_data="Shikimori_"),
        InlineKeyboardButton(text=" 👒𝔽𝕖𝕒𝕥𝕦𝕣𝕖𝕤", callback_data="help_back"),
    ],
    [
        InlineKeyboardButton(text="💞𝕊𝕦𝕡𝕡𝕠𝕣𝕥 𝕘𝕣𝕡", url=f"https://t.me/{SUPPORT_CHAT}"),
        InlineKeyboardButton(text="🆙 𝕌𝕡𝕕𝕒𝕥𝕖𝕤", url=f"https://t.me/{UPDATE_CHANNEL}"),
   
    ], 
]

def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="Go Back", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            hmm = "𝙺𝚘𝚗𝚒𝚌𝚑𝚒𝚠𝚊 {}".format(escape_markdown(first_name))
            HMM = hmm + PM_START_TEXT

            update.effective_message.reply_photo(
                START_MEDIA,
                HMM,                        
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    else:
        start_buttons = [
                 [
                    InlineKeyboardButton(text="💞𝕊𝕦𝕡𝕡𝕠𝕣𝕥 𝕘𝕣𝕡", url=f"https://t.me/{SUPPORT_CHAT}"),
                    InlineKeyboardButton(text=" 🆙𝕌𝕡𝕕𝕒𝕥𝕖𝕤", url=f"https://t.me/{UPDATE_CHANNEL}")
                 ]
                ]
        chat_id = update.effective_chat.id
        first_name = update.effective_user.first_name
        chat_name = dispatcher.bot.getChat(chat_id).title
        start_text= "Hello {}\nI Am 𝙰𝚕𝚒𝚟𝚎 𝚜𝚒𝚗𝚌𝚎: {}\n".format(escape_markdown(first_name), uptime)
        try:
            if start_id in ("jpeg", "jpg", "png"):
                update.effective_message.reply_photo(
                    START_MEDIA, caption = start_text, reply_markup=InlineKeyboardMarkup(start_buttons),
                parse_mode=ParseMode.MARKDOWN,
            )
            elif start_id in ("mp4", "mkv"):
                update.effective_message.reply_video(
                START_MEDIA, caption = start_text, reply_markup=InlineKeyboardMarkup(start_buttons),
                parse_mode=ParseMode.MARKDOWN,
            )
            elif start_id in ("gif", "webp"):
                update.effective_message.reply_animation(
                START_MEDIA, caption = start_text, reply_markup=InlineKeyboardMarkup(start_buttons),
                parse_mode=ParseMode.MARKDOWN,
            )
            else:
                update.effective_message.reply_text(start_text, reply_markup=InlineKeyboardMarkup(start_buttons),
                parse_mode=ParseMode.MARKDOWN,)

        except:
            update.effective_message.reply_text(START_MEDIA, caption = start_text, reply_markup=InlineKeyboardMarkup(start_buttons),
                parse_mode=ParseMode.MARKDOWN,)

start_handler = CommandHandler("start", start, run_async=True)
dispatcher.add_handler(start_handler)

def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )

def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )