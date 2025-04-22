import asyncio
import logging
import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, STICKER_ID
from utils.sticker import check_sticker

# Escape untuk MarkdownV2
def escape_markdown_v2(text: str) -> str:
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f"([{re.escape(escape_chars)}])", r'\\\1', text)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Init bot
app = Client(
    "blakeshley_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- /start command ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    chat_id = message.chat.id

    try:
        text1 = "༄❀ Delicate petals drift around you... ᯓ༄"
        msg1 = await client.send_message(chat_id, text1, parse_mode="HTML")
        await asyncio.sleep(3)
        await msg1.delete()

        if await check_sticker(client, STICKER_ID):
            sticker_msg = await client.send_sticker(chat_id, STICKER_ID)
            await asyncio.sleep(3)
            await sticker_msg.delete()
        else:
            msg2 = await client.send_message(
                chat_id,
                "⚠️ Sihir gagal... stiker tidak bisa dikirim ~",
                parse_mode="HTML"
            )
            await asyncio.sleep(3)
            await msg2.delete()

        text2 = "༄ Feathers of dreams flutter in the twilight ~ ❀༄"
        msg3 = await client.send_message(chat_id, text2, parse_mode="HTML")
        await asyncio.sleep(3)
        await msg3.delete()

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ᯓ ✎ format your wishes ✎", callback_data="format")]
        ])

        await client.send_message(
            chat_id,
            "𖤓 Pilih pesonamu, wahai pengelana ~",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    except Exception as e:
        logging.error(f"Terjadi kesalahan saat start: {e}")

# --- Format order handler ---
@app.on_callback_query(filters.regex("format"))
async def format_button(client, callback_query):
    try:
        await callback_query.answer("Menyiapkan format...")

        username = callback_query.from_user.username or "username"
        text = (
            f"Salutations I'm @{username}, I’d like to place an order for catalog t.me/blakeshley listed at Blakeshley, "
            f"Using payment method [dana, gopay, qriss, spay, ovo, bank.] "
            f"The total comes to IDR [00.000] Inrush add 5k [yay/nay]. "
            f"Kindly process this, Thanks a bunch."
        )

        escaped_text = escape_markdown_v2(text)
        message_content = f"*Copy and Paste This:*\n\n```{escaped_text}```"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ᯓ ✎ Copy Here", switch_inline_query=text)]
        ])

        sent = await client.send_message(
            callback_query.message.chat.id,
            message_content,
            parse_mode="MarkdownV2",
            reply_markup=keyboard
        )

        await asyncio.sleep(420)  # 7 menit
        await sent.delete()

        try:
            await callback_query.message.delete()
        except Exception as e:
            logging.warning(f"Gagal hapus pesan tombol format: {e}")

        await client.send_message(
            callback_query.message.chat.id,
            "༄ Sihir memudar ke dalam kabut... ༄",
            parse_mode="HTML"
        )

    except Exception as e:
        logging.error(f"Terjadi kesalahan dalam tombol format: {e}")

# --- Jalankan bot ---
if __name__ == "__main__":
    app.run()