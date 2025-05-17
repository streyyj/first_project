# meta developer: @streyyj

from hikkatl.types import Message
from .. import loader

@loader.tds
class AutoMatchLastMod(loader.Module):
    strings = {"name": "AutoMatchLast"}

    async def automatchlastcmd(self, message: Message):
        chat = "@F_CardBot"

        # Получаем последнее сообщение от бота
        async for msg in self.client.iter_messages(chat, limit=10):
            if msg.from_id and hasattr(msg.from_id, "user_id"):
                # Можно заменить на ID бота, если знаешь (например: 123456789)
                if msg.from_id.user_id == 6354447504:  # ← замените на ID F_CardBot при необходимости
                    if msg.buttons:
                        for row in msg.buttons:
                            for button in row:
                                if "🎮 Играть матч" in button.text:
                                    await button.click()
                                    return await message.edit("✅ Нажал на 'Играть матч'")
                    return await message.edit("❌ Кнопка '🎮 Играть матч' не найдена.")
        
        await message.edit("❌ Не найдено последнее сообщение от бота.")
