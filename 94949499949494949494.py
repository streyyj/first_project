# -*- coding: utf-8 -*-
from .. import loader, utils
import asyncio

@loader.tds
class FCMatchMod(loader.Module):
    """Модуль для автоклика игры \"Матч\" бота @F_CardBot."""
    strings = {"name": "FCMatch"}

    async def client_ready(self, client, db):
        self.client = client

    async def fcmatchcmd(self, message):
        """Запуск сценария автоклика для команды .fcmatch."""
        chat = message.chat
        # Отправляем сообщение "Меню" в текущий чат
        await self.client.send_message(chat, "Меню")
        # Ждём 5 секунд для получения ответа от бота
        await asyncio.sleep(5)
        # Поиск сообщения от бота с кнопкой "⚽️Матч"
        target_msg = None
        msgs = await self.client.get_messages(chat, limit=5, from_user='F_CardBot')
        for m in msgs:
            if m.buttons:
                for row in m.buttons:
                    for btn in row:
                        if getattr(btn, 'text', '') == '⚽️Матч':
                            target_msg = m
                            break
                    if target_msg:
                        break
                if target_msg:
                    break
        # Если сообщение найдено, нажимаем кнопку "⚽️Матч"
        if target_msg:
            await target_msg.click(text='⚽️Матч')
        # Ждём ещё 5 секунд для следующего ответа
        await asyncio.sleep(5)
        # Поиск сообщения от бота с кнопкой "🎮Играть матч"
        target_msg2 = None
        msgs = await self.client.get_messages(chat, limit=5, from_user='F_CardBot')
        for m in msgs:
            if m.buttons:
                for row in m.buttons:
                    for btn in row:
                        if getattr(btn, 'text', '') == '🎮Играть матч':
                            target_msg2 = m
                            break
                    if target_msg2:
                        break
                if target_msg2:
                    break
        # Если сообщение найдено, нажимаем кнопку "🎮Играть матч"
        if target_msg2:
            await target_msg2.click(text='🎮Играть матч')
