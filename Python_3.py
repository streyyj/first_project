from telethon.sync import TelegramClient
from telethon.tl.functions.messages import SendMessageRequest

# Твои данные
api_id = 1234567  # замени на свой api_id
api_hash = 'ваш_api_hash'  # замени на свой api_hash
bot_username = '@F_CardBot'

async def send_menu():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        await client.start()
        print("Клиент запущен")
        await client(SendMessageRequest(
            peer=bot_username,
            message='Меню'
        ))
        print("Сообщение 'Меню' отправлено!")