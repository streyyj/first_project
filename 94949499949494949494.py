# -*- coding: utf-8 -*-
from .. import loader, utils
import asyncio

@loader.tds
class FCMatchMod(loader.Module):
    """Модуль для автоклика 'Матча' бота @F_CardBot."""
    strings = {"name": "FCMatch"}

    async def client_ready(self, client, db):
        self.client = client

    async def fcmatchcmd(self, message):
        """Команда: .fcmatch — Автоматически запускает матч в @F_CardBot."""
        chat = message.chat

        # Шаг 1: Отправляем "Меню"
        await self.client.send_message(chat, "Меню")
        await asyncio.sleep(5)

        # Шаг 2: Ищем сообщение от @F_CardBot с кнопкой "⚽️ Матч"
        match_msg = None
        async for msg in self.client.iter_messages(chat, from_user="F_CardBot", limit=10):
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if button.text == "⚽️ Матч":
                            match_msg = msg
                            break
                    if match_msg:
                        break
            if match_msg:
                break

        if not match_msg:
            await message.edit("❌ Не удалось найти кнопку '⚽️ Матч'.")
            return

        await match_msg.click(text="⚽️ Матч")
        await asyncio.sleep(5)

        # Шаг 3: Ищем сообщение от @F_CardBot с кнопкой "🎮 Играть матч"
        play_msg = None
        async for msg in self.client.iter_messages(chat, from_user="F_CardBot", limit=10):
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if button.text == "🎮 Играть матч":
                            play_msg = msg
                            break
                    if play_msg:
                        break
            if play_msg:
                break

        if not play_msg:
            await message.edit("❌ Не удалось найти кнопку '🎮 Играть матч'.")
            return

        await play_msg.click(text="🎮 Играть матч")
        await message.edit("✅ Матч успешно запущен.")
