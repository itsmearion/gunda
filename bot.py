import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, STICKER_ID
from utils.sticker import check_sticker

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Inisialisasi Bot
app = Client(
    "blakeshley_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- Start Command ---
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    chat_id = message.chat.id

    try:
        # Teks pertama
        first_msg = await client.send_message(chat_id, "༄❀ delicate petals drift around you\\.\\.\\. ᯓ༄", parse_mode="MarkdownV2")
        await asyncio.sleep(3)
        await first_msg.delete()

        # Sticker aesthetic
        if await check_sticker(client, STICKER_ID):
            sticker_msg = await client.send_sticker(chat_id, STICKER_ID)
            await asyncio.sleep(3)
            await sticker_msg.delete()
        else:
            warning_msg = await client.send_message(chat_id, "⚠️ sihir gagal\\.\\.\\. stiker tidak bisa dikirim \\~",", parse_mode="MarkdownV2")
            await asyncio.sleep(3)
            await warning_msg.delete()

        # Teks kedua
        second_msg = await client.send_message(chat_id, "༄ feathers of dreams flutter in the twilight \\~ ❀༄", parse_mode="MarkdownV2")
        await asyncio.sleep(3)
        await second_msg.delete()

        # Menu button
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ᯓ ✎ format your wishes ✎", callback_data="format")]
        ])
        await client.send_message(
            chat_id,
            "𖤓 pilih pesonamu, wahai pengelana \\~",
            reply_markup=keyboard,
            parse_mode="MarkdownV2"
        )

    except Exception as e:
        logging.error(f"Terjadi kesalahan saat start: {e}")

# --- Format Order Button ---
@app.on_callback_query(filters.regex("format"))
async def format_button(client, callback_query):
    try:
        await callback_query.answer()
        username = callback_query.from_user.username or "username"

        text = (
            f"Salutations I\\'m @{username}, I’d like to place an order for catalog t\\.me/blakeshley listed at Blakeshley, "
            f"Using payment method \dana, gopay, qriss, spay, ovo, bank\\.\ "
            f"The total comes to IDR \00\\.000\ Inrush add 5k \yay/nay\\\. "
            f"Kindly process this, Thanks a bunch\\."
        )

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ᯓ ✎ Copy Here", switch_inline_query_current_chat=text)]
        ])

        formatted_text = f"*Copy and Paste This:*\n\n```{text}```"
        sent = await callback_query.message.reply_text(
            formatted_text,
            parse_mode="MarkdownV2",
            reply_markup=keyboard
        )

        # Tunggu 7 menit
        await asyncio.sleep(420)

        await sent.delete()
        try:
            await callback_query.message.delete()
        except Exception as e:
            logging.warning(f"Gagal menghapus pesan tombol format: {e}")

        await client.send_message(
            callback_query.message.chat.id,
            "༄ sihir memudar ke dalam kabut\\.\\.\\. ༄",
            parse_mode="MarkdownV2"
        )

    except Exception as e:
        logging.error(f"Terjadi kesalahan dalam alur tombol format: {e}")

# --- Unit Test ---
if __name__ == "__main__" and False:  # Ganti ke True untuk testing manual
    test_cases = [
        "*bold*",
        "_italic_",
        "[link](https://example.com)",
        "~strike~",
        "`code`",
        "special chars !(){}[]-_.",
        "Salutations I'm @user, pay via [gopay].",
    ]

    print("Testing escape_markdown_v2()...")
    for i, case in enumerate(test_cases, 1):
        escaped = escape_markdown_v2(case)
        print(f"{i}. Original : {case}")
        print(f"   Escaped  : {escaped}\n")

# --- Jalankan Bot ---
if __name__ == "__main__":
    app.run()