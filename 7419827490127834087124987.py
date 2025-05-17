from hikkatl.types import Message
from .. import loader, utils
import asyncio

@loader.tds
class AutoMatchMod(loader.Module):
    strings = {"name": "AutoMatch"}

    async def automatchcmd(self, m: Message):
        chat = "@F_CardBot"  # чат с ботом

        # Шаг 1: отправляем "Меню"
        await self.client.send_message(chat, "Меню")
        await asyncio.sleep(2)

        # Шаг 2: ищем кнопку "⚽️ Матч" и жмём
        async for msg in self.client.iter_messages(chat, from_user="F_CardBot", limit=5):
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if "⚽️ Матч" in button.text:
                            await button.click()
                            await asyncio.sleep(2)  # даём время на редактирование
                            break
                break  # выходим из цикла, кнопку нашли и нажали

        # Шаг 3: получаем последнее сообщение снова, т.к. оно было отредактировано
        latest = (await self.client.get_messages(chat, from_user="F_CardBot", limit=1))[0]

        # Шаг 4: ищем кнопку "🎮 Играть матч" и жмём
        if latest.buttons:
            for row in latest.buttons:
                for button in row:
                    if "🎮 Играть матч" in button.text:
                        await button.click()
                        return await m.edit("✅ Матч начат!")

        await m.edit("❌ Кнопка '🎮 Играть матч' не найдена.")
