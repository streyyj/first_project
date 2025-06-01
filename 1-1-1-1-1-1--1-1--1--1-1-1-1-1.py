# coding: utf-8
from telethon import events, Button
from .. import loader, utils

class FCModule(loader.Module):
    """Module for automating interaction with @F_CardBot (учёт кнопок без пробела)"""
    strings = {"name": "FCModule"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.unrestricted
    async def fccmd(self, message):
        """
        .fc - автоматизация:
        1) Отправляет "Меню"
        2) Нажимает кнопку "⚽️Матч"
        3) Ждёт редактирования того же сообщения и нажимает кнопку "🎮Играть матч"
        """
        chat = await message.get_chat()

        # 1) Отправляем "Меню"
        await self.client.send_message(chat, "Меню")

        BOT_USERNAME = "F_CardBot"

        # 2) Ждём новое сообщение от бота
        try:
            response = await self.client.wait_event(
                events.NewMessage(from_users=BOT_USERNAME, chats=chat),
                timeout=10
            )
        except Exception:
            await message.edit("<b>Ошибка:</b> не пришёл ответ от бота (NewMessage).")
            return

        # 2.1) Ищем кнопку "⚽️Матч" (без пробела)
        if not response.buttons:
            await message.edit("<b>Ошибка:</b> бот прислал сообщение без кнопок.")
            return

        found_match = False
        for row in response.buttons:
            for btn in row:
                text = btn.text.strip()
                if text == "⚽️Матч":
                    await response.click(text="⚽️Матч")
                    found_match = True
                    break
            if found_match:
                break

        if not found_match:
            await message.edit("<b>Ошибка:</b> не удалось найти кнопку '⚽️Матч'.")
            return

        # 3) Ждём, когда бот отредактирует то же сообщение
        try:
            edited = await self.client.wait_event(
                events.MessageEdited(from_users=BOT_USERNAME, chats=chat),
                timeout=10
            )
        except Exception:
            await message.edit("<b>Ошибка:</b> не дождались отредактированного сообщения.")
            return

        # 3.1) Ищем кнопку "🎮Играть матч" (без пробела) и нажимаем её
        if not edited.buttons:
            await message.edit("<b>Ошибка:</b> в отредактированном сообщении нет кнопок.")
            return

        found_play = False
        for row in edited.buttons:
            for btn in row:
                text = btn.text.strip()
                if text == "🎮Играть матч":
                    await edited.click(text="🎮Играть матч")
                    found_play = True
                    break
            if found_play:
                break

        if not found_play:
            await message.edit("<b>Ошибка:</b> не удалось найти кнопку '🎮Играть матч'.")
            return

        await message.edit("<b>Выполнено:</b> нажаты «⚽️Матч» и «🎮Играть матч».")
