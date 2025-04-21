from pyrogram.errors import StickersetInvalid

async def check_sticker(client, sticker_id):
    try:
        await client.get_messages("me", sticker_id)
        return True
    except StickersetInvalid:
        return False
    except Exception:
        return False