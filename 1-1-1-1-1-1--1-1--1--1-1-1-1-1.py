# coding: utf-8
from telethon import events, Button
from .. import loader, utils


class FCModule(loader.Module):
    """Module for automating interaction with @F_CardBot"""
    strings = {"name": "FCModule"}

    async def client_ready(self, client, db):
        # Сохраняем клиент в self для дальнейшего использования
        self.client = client
        self.db = db

    @loader.unrestricted  # разрешаем запускать команду в любом чате
    async def fccmd(self, message):
        """
        .fc - автоматическая последовательность:
        1) Отправляет "Меню"
        2) Нажимает кнопку "⚽️ Матч"
        3) Ждёт редактирования и нажимает кнопку "🎮 Играть матч"
        """
        # 0) Получаем информацию о чате, где команда была вызвана
        chat = await message.get_chat()
        me = await self.client.get_me()

        # 1) Отправляем "Меню" в тот же чат, где вызвана команда
        #    (предполагается, что в этом же чате присутствует @F_CardBot)
        sent = await self.client.send_message(chat, "Меню")

        # 2) Ждём нового сообщения от @F_CardBot
        #    Параметр from_users указываем либо ID бота, либо строковый username.
        BOT_USERNAME = "F_CardBot"
        try:
            response: events.newmessage.NewMessage.Event = await self.client.wait_event(
                events.NewMessage(from_users=BOT_USERNAME, chats=chat),
                timeout=10
            )
        except Exception:
            await message.edit("<b>Ошибка:</b> не удалось получить ответ от бота (NewMessage).")
            return

        # 2.1) В полученном сообщении ищем кнопку c текстом "⚽️ Матч" и кликаем по ней.
        if not response.buttons:
            await message.edit("<b>Ошибка:</b> бот прислал сообщение без кнопок.")
            return

        found_match = False
        for row in response.buttons:
            for btn in row:
                if btn.text.strip() == "⚽️ Матч":
                    # Кликаем (отправляем callback_query)
                    await response.click(text="⚽️ Матч")
                    found_match = True
                    break
            if found_match:
                break

        if not found_match:
            await message.edit("<b>Ошибка:</b> не удалось найти кнопку '⚽️ Матч'.")
            return

        # 3) После того, как мы нажали "⚽️ Матч", бот редактирует то же самое сообщение.
        #    Отслеживаем событие MessageEdited от @F_CardBot
        try:
            edited: events.messageedited.MessageEdited.Event = await self.client.wait_event(
                events.MessageEdited(from_users=BOT_USERNAME, chats=chat),
                timeout=10
            )
        except Exception:
            await message.edit("<b>Ошибка:</b> не дождались отредактированного сообщения от бота.")
            return

        # 3.1) В обновлённом сообщении ищем кнопку "🎮 Играть матч" и кликаем по ней.
        if not edited.buttons:
            await message.edit("<b>Ошибка:</b> в отредактированном сообщении нет кнопок.")
            return

        found_play = False
        for row in edited.buttons:
            for btn in row:
                if btn.text.strip() == "🎮 Играть матч":
                    await edited.click(text="🎮 Играть матч")
                    found_play = True
                    break
            if found_play:
                break

        if not found_play:
            await message.edit("<b>Ошибка:</b> не удалось найти кнопку '🎮 Играть матч'.")
            return

        # Всё успешно
        await message.edit("<b>Выполнено:</b> нажаты «⚽️ Матч» и «🎮 Играть матч».")
