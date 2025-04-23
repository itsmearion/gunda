import asyncio
import logging
import re

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import API_ID, API_HASH, BOT_TOKEN

# --- Setup logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# --- Escape MarkdownV2 special characters ---
def escape_markdown(text: str) -> str:
    return re.sub(r'([_*[\]()~`>#+=|{}.!\\-])', r'\\\1', text)

# --- Initialize bot ---
app = Client(
    "blakeshley_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode="MarkdownV2"
)

# --- Helper: auto delete message after delay ---
async def auto_delete(message, delay: int = 420):
    try:
        await asyncio.sleep(delay)
        await message.delete()
    except Exception as e:
        logging.warning(f"Gagal hapus pesan otomatis: {e}")

# --- /start command handler ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    chat_id = message.chat.id

    try:
        text1 = "༄❀ delicate petals drift around you... ᯓ༄"
        msg1 = await client.send_message(chat_id, escape_markdown(text1))
        asyncio.create_task(auto_delete(msg1, 3))

        if await check_sticker(client, STICKER_ID):
            sticker_msg = await client.send_sticker(chat_id, STICKER_ID)
            asyncio.create_task(auto_delete(sticker_msg, 3))
        else:
            msg2 = await client.send_message(
                chat_id,
                escape_markdown("⚠️ sihir gagal... stiker tidak bisa dikirim ~")
            )
            asyncio.create_task(auto_delete(msg2, 3))

        text2 = "༄ feathers of dreams flutter in the twilight ~ ❀༄"
        msg3 = await client.send_message(chat_id, escape_markdown(text2))
        asyncio.create_task(auto_delete(msg3, 3))

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ᯓ ✎ format your wishes ✎", callback_data="format")]
        ])

        await client.send_message(
            chat_id,
            escape_markdown("𖤓 pilih pesonamu, wahai pengelana ~"),
            reply_markup=keyboard
        )

    except Exception as e:
        logging.error(f"Terjadi kesalahan saat start: {e}")

# --- Format button callback handler ---
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

        escaped_text = escape_markdown(text)
        message_content = f"*Copy and Paste This:*\n\n```{escaped_text}```"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ᯓ ✎ Copy Here", switch_inline_query=text)]
        ])

        sent = await client.send_message(
            callback_query.message.chat.id,
            message_content,
            reply_markup=keyboard
        )

        # Auto delete in 7 minutes
        asyncio.create_task(auto_delete(sent, 420))

        # Try delete the button message
        try:
            await callback_query.message.delete()
        except Exception as e:
            logging.warning(f"Gagal hapus pesan tombol format: {e}")

        msg = await client.send_message(
            callback_query.message.chat.id,
            escape_markdown("༄ sihir memudar ke dalam kabut... ༄")
        )
        asyncio.create_task(auto_delete(msg, 3))

    except Exception as e:
        logging.error(f"Terjadi kesalahan dalam tombol format: {e}")

# --- Run bot ---
if __name__ == "__main__":
    app.run()