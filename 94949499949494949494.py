# meta developer: @yourusername
# requires: hikka

from .. import loader, utils
import asyncio

class FCardAutoMatchMod(loader.Module):
    """Автоматически запускает матч в F_CardBot"""
    strings = {"name": "FCardAutoMatch"}

    async def client_ready(self, client, db):
        self.client = client

    async def fcmatchcmd(self, message):
        """Отправляет 'Меню' и жмёт на кнопки ⚽️ Матч → 🎮 Играть матч"""
        await message.edit("Запускаю матч...")

        chat = message.chat_id

        # Шаг 1: отправляем "Меню"
        menu_msg = await self.client.send_message(chat, "Меню")

        # Шаг 2: ждём 5 секунд
        await asyncio.sleep(5)

        # Шаг 3: находим сообщение от бота с кнопкой "⚽️ Матч"
        bot_msg = None
        async for msg in self.client.iter_messages(chat, from_user="F_CardBot", limit=10):
            if msg.buttons:
                for row in msg.buttons:
                    for btn in row:
                        if btn.text.strip() == "⚽️ Матч":
                            bot_msg = msg
                            break
                    if bot_msg:
                        break
            if bot_msg:
                break

        if not bot_msg:
            await message.edit("❌ Не удалось найти кнопку '⚽️ Матч'")
            return

        # Шаг 4: нажимаем "⚽️ Матч"
        for row in bot_msg.buttons:
            for btn in row:
                if btn.text.strip() == "⚽️ Матч":
                    await btn.click()
                    break

        # Шаг 5: ждём 5 секунд
        await asyncio.sleep(5)

        # Шаг 6: находим редактированное сообщение с кнопкой "🎮 Играть матч"
        match_msg = None
        async for msg in self.client.iter_messages(chat, from_user="F_CardBot", limit=10):
            if msg.buttons:
                for row in msg.buttons:
                    for btn in row:
                        if btn.text.strip() == "🎮 Играть матч":
                            match_msg = msg
                            break
                    if match_msg:
                        break
            if match_msg:
                break

        if not match_msg:
            await message.edit("❌ Не удалось найти кнопку '🎮 Играть матч'")
            return

        # Шаг 7: нажимаем "🎮 Играть матч"
        for row in match_msg.buttons:
            for btn in row:
                if btn.text.strip() == "🎮 Играть матч":
                    await btn.click()
                    break

        await message.edit("✅ Матч запущен!")
