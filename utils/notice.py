import asyncio

async def delay_notice(client, chat_id, message_id):
    await asyncio.sleep(3600)  # 1 jam
    try:
        await client.send_message(chat_id, "༄ a soft breeze stirs the silence... ༄", reply_to_message_id=message_id)
    except Exception:
        pass