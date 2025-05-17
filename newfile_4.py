# meta developer: @streyyj

from hikkatl.types import Message
from .. import loader

@loader.tds
class AutoMatchLastMod(loader.Module):
    strings = {"name": "AutoMatchLast"}

    async def automatchlastcmd(self, message: Message):
        chat = message.chat.id  # текущий чат

        async for msg in self.client.iter_messages(chat, limit=10):
            # Проверяем наличие кнопки "Играть матч"
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if "Играть матч" in button.text:
                            await button.click()
                            return await message.edit("✅ Нажал на 'Играть матч'")
        await message.edit("❌ Не найдено сообщение с кнопкой 'Играть матч'")
