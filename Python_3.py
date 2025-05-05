from telethon.sync import TelegramClient
from telethon.tl.functions.messages import SendMessageRequest

# Замени на свои данные
api_id = 1234567  # Твой API ID
api_hash = 'ваш_api_hash'  # Твой API Hash
bot_username = '@F_CardBot'

# Создаем клиент
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Отправляем сообщение боту
    await client(SendMessageRequest(
        peer=bot_username,
        message='Меню'
    ))
    print("Сообщение 'Меню' отправлено боту!")

# Запускаем клиент
with client:
    client.loop.run_until_complete(main())