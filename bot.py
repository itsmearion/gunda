import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, STICKER_ID
from utils.sticker import check_sticker
from html import escape

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Init Bot
app = Client(
    "blakeshley_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- Start Command ---
@app.on_message(filters.command("start"))
async def start(client, message):
    chat_id = message.chat.id
    awakening = await message.reply_text("ᯓ ᡣ𐭩 shhh... the winds are whispering ~ please wait, little soul...")
    await asyncio.sleep(2)
    await awakening.delete()

    # Kirim sticker aesthetic
    if await check_sticker(client, STICKER_ID):
        await client.send_sticker(chat_id, STICKER_ID)
    else:
        await message.reply_text("⚠️ the magic faltered... sticker could not be sent ~")

    await asyncio.sleep(1)
    await message.reply_text("༄❀ delicate petals drift around you... ᯓ༄")
    await asyncio.sleep(1)
    await message.reply_text("༄ feathers of dreams flutter in the twilight ~ ❀༄")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("ᯓ ✎ format your wishes ✎", callback_data="format")]
    ])
    await message.reply_text(
        "𖤓 pick your charm, dear traveller ~",
        reply_markup=keyboard
    )

# --- Format Order Button ---
@app.on_callback_query(filters.regex("format"))
async def format_button(client, callback_query):
    try:
        await callback_query.answer()
        username = callback_query.from_user.username or "username"

        text = (
            f"Salutations I'm @{username}, I’d like to place an order for catalog t.me/blakeshley listed at Blakeshley, "
            f"Using payment method [dana, gopay, qriss, spay, ovo, bank.] "
            f"The total comes to IDR [00.000] Inrush add 5k [yay/nay]. "
            f"Kindly process this, Thanks a bunch."
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ᯓ ✎ Copy Here", switch_inline_query_current_chat=text)]
        ])

        sent = await callback_query.message.reply_text(
            f"<b>Copy and Paste This:</b>\n\n<code>{escape(text)}</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )

        await asyncio.sleep(420)  # 7 menit
        await sent.delete()

        try:
            await callback_query.message.delete()
        except Exception as e:
            logging.warning(f"Failed to delete format button message: {e}")

        await client.send_message(
            callback_query.message.chat.id,
            "༄ the magic fades into the mist... ༄"
        )

    except Exception as e:
        logging.error(f"Error in format button flow: {e}")

# --- Run Bot ---
app.run()