# meta developer: @yourusername

from .. import loader
import asyncio

class FCardSimpleMatchMod(loader.Module):
    """Авто-матч в @F_CardBot без зависимостей"""
    strings = {"name": "FCardSimpleMatch"}

    async def fcmatchcmd(self, message):
        """Запускает матч: Меню → Матч → Играть матч"""
        chat = message.chat_id
        await message.edit("⚽️ Запускаю матч...")

        # 1. Отправляем 'Меню'
        await self.client.send_message(chat, "Меню")
        await asyncio.sleep(3)

        # 2. Ищем кнопку '⚽️ Матч'
        msg1 = None
        async for msg in self.client.iter_messages(chat, from_user="F_CardBot", limit=5):
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if "⚽️ Матч" in button.text:
                            msg1 = msg
                            await button.click()
                            await asyncio.sleep(3)
                            break
                    if msg1:
                        break
            if msg1:
                break

        if not msg1:
            return await message.edit("❌ Не нашёл кнопку '⚽️ Матч'")

        # 3. Ищем кнопку '🎮 Играть матч'
        msg2 = None
        async for msg in self.client.iter_messages(chat, from_user="F_CardBot", limit=5):
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if "🎮 Играть матч" in button.text:
                            msg2 = msg
                            await button.click()
                            return await message.edit("✅ Матч сыгран!")

        await message.edit("❌ Не нашёл кнопку '🎮 Играть матч'")
