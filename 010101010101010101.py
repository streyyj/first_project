from hikkatl.types import Message
from hikkatl.utils import sleep
from hikkatl import loader

@loader.tds
class FootCardMod(loader.Module):
    """Автоматизация матчей в @F_CardBot"""
    strings = {"name": "FootCardAuto"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.command()
    async def fcmatch(self, message: Message):
        """Запустить автоматизацию матча"""
        # Шаг 1: Отправка "Меню"
        await self.client.send_message("@F_CardBot", "Меню")
        await sleep(5)

        # Шаг 2: Поиск и нажатие кнопки "⚽️Матч"
        async for msg in self.client.iter_messages("@F_CardBot", limit=3):
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if "⚽️Матч" in button.text:
                            await msg.click(0)
                            await sleep(5)
                            break

        # Шаг 3: Поиск и нажатие кнопки "🎮Играть матч"
        async for msg in self.client.iter_messages("@F_CardBot", limit=3):
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if "🎮Играть матч" in button.text:
                            await msg.click(0)
                            return