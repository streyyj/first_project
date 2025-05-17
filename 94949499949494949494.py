# meta developer: @yourusername

from .. import loader
import asyncio

class FCardSimpleMatchMod(loader.Module):
    """Автоматически запускает матч в @F_CardBot"""
    strings = {"name": "FCardSimpleMatch"}

    async def fcmatchcmd(self, message):
        """Запускает матч: Меню → Матч → Играть матч"""
        await message.edit("⏳ Запуск...")

        chat = message.chat_id

        # Шаг 1: отправляем 'Меню'
        await self.client.send_message(chat, "Меню")
        await asyncio.sleep(3)

        # Шаг 2: ищем кнопку '⚽️ Матч'
        async for msg in self.client.iter_messages(chat, from_user="F_CardBot", limit=10):
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if "⚽️ Матч" in button.text:
                            await button.click()
                            await asyncio.sleep(3)
                            break
                    else:
                        continue
                    break
            else:
                continue
            break

        # Шаг 3: ищем кнопку '🎮 Играть матч'
        async for msg in self.client.iter_messages(chat, from_user="F_CardBot", limit=10):
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if "🎮 Играть матч" in button.text:
                            await button.click()
                            await message.edit("✅ Матч сыгран!")
                            return

        await message.edit("❌ Кнопка '🎮 Играть матч' не найдена")
