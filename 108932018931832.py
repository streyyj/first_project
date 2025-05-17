from hikkatl.types import Message
from hikkatl import loader
import asyncio

@loader.tds
class FootCardAutoMod(loader.Module):
    """Автоматизация матчей в @F_CardBot"""
    strings = {"name": "FootCardAuto"}

    async def client_ready(self, client, db):
        self.client = client

    async def find_button(self, text: str, limit: int = 5):
        """Поиск кнопки в последних сообщениях"""
        async for msg in self.client.iter_messages("@F_CardBot", limit=limit):
            if not msg.buttons:
                continue
            for row in msg.buttons:
                for button in row:
                    if text in button.text:
                        return msg
        return None

    @loader.command()
    async def fcmatch(self, message: Message):
        """Запустить автоматизацию матча"""
        # Шаг 1: Отправка "Меню"
        await self.client.send_message("@F_CardBot", "Меню")
        await asyncio.sleep(5)

        # Шаг 2: Нажатие "⚽️Матч"
        match_msg = await self.find_button("⚽️Матч")
        if match_msg:
            await match_msg.click(0)
            await asyncio.sleep(5)

            # Шаг 3: Нажатие "🎮Играть матч"
            play_msg = await self.find_button("🎮Играть матч")
            if play_msg:
                await play_msg.click(0)
                await message.edit("✅ Матч запущен!")
            else:
                await message.edit("❌ Не найдена кнопка '🎮Играть матч'")
        else:
            await message.edit("❌ Не найдена кнопка '⚽️Матч'")