# coding: utf-8
from telethon import events, Button
from .. import loader

class FCModule(loader.Module):
    """Module for automating interaction with @F_CardBot (улучшенный вариант)"""
    strings = {"name": "FCModule"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

        # 1. Получаем сущность бота и сохраняем его ID
        try:
            bot_entity = await self.client.get_entity("F_CardBot")
            self.bot_id = bot_entity.id
        except Exception as e:
            # Если не удалось получить entity, то при попытке .fc всегда будет ошибка
            self.bot_id = None
            self.log(f"⚠️ Не удалось получить entity @F_CardBot: {e}", "error")

    @loader.unrestricted
    async def fccmd(self, message):
        """
        .fc - автоматическая последовательность:
        1) Отправляет "Меню"
        2) Ждёт ответа от бота и нажимает кнопку "⚽️Матч"
        3) Ждёт, пока бот тот же message отредактирует, и нажимает "🎮Играть матч"
        """
        if not self.bot_id:
            await message.edit("<b>Ошибка:</b> не удалось найти @F_CardBot (не знаю, куда слать callback).")
            return

        # 0) Получаем объект чата, куда была вызвана команда
        chat = await message.get_chat()

        # 1) Отправляем "Меню" и сохраняем исходное сообщение
        sent = await self.client.send_message(chat, "Меню")

        # Удалим (или отпишем) сообщение с инструкцией, чтобы видеть только логи
        await message.delete()

        # 2) Ждём, пока придёт NEW_MESSAGE от нашего бота, и проверяем, что он
        # ответил именно на наше "Меню"
        #
        # Здесь мы слушаем все новые сообщения от bot_id в любой комнате, но
        # проверяем внутри, что reply_to_msg_id == sent.id
        #
        try:
            while True:
                response_event = await self.client.wait_event(
                    events.NewMessage(from_users=self.bot_id),
                    timeout=15  # если за 15 секунд бот не ответил — выходим
                )
                response = response_event.message

                # Проверяем, что бот ответил именно на наше "Меню"
                if response.reply_to_msg_id == sent.id:
                    break
                # Иначе просто продолжаем цикл и ждём дальше (если timeout не сработал)
        except Exception:
            # Ловим либо TimeoutError, либо что‑то ещё
            await self.client.send_message(chat, "<b>Ошибка:</b> не пришёл ответ от бота (NewMessage).")
            return

        # 2.1) В полученном ответе ищем кнопку "⚽️Матч" (учитываем, что между эмодзи и текстом
        # может не быть пробела: "⚽️Матч" или "⚽️ Матч", поэтому сверим сразу оба варианта).
        if not response.buttons:
            await self.client.send_message(chat, "<b>Ошибка:</b> бот прислал сообщение без кнопок.")
            return

        found_match = False
        for row in response.buttons:
            for btn in row:
                btn_text = btn.text.strip()
                if btn_text in ("⚽️Матч", "⚽️ Матч"):
                    await response.click(text=btn_text)
                    found_match = True
                    break
            if found_match:
                break

        if not found_match:
            await self.client.send_message(chat, "<b>Ошибка:</b> не найдена кнопка '⚽️Матч'.")
            return

        # 3) Ждём, пока бот ОТРЕДАКТИРУЕТ то же сообщение (MessageEdited) и
        # проверяем, что это снова сообщение-ответ на наш sent.id
        try:
            while True:
                edited_event = await self.client.wait_event(
                    events.MessageEdited(from_users=self.bot_id),
                    timeout=15
                )
                edited = edited_event.message

                # Тут бот редактирует то же самое сообщение, поэтому reply_to_msg_id
                # у редактированного должен быть всё тот же sent.id
                if edited.reply_to_msg_id == sent.id:
                    break
        except Exception:
            await self.client.send_message(chat, "<b>Ошибка:</b> не дождались отредактированного сообщения.")
            return

        # 3.1) В отредактированном ищем кнопку "🎮Играть матч" (учтём обе версии)
        if not edited.buttons:
            await self.client.send_message(chat, "<b>Ошибка:</b> отредактированное сообщение без кнопок.")
            return

        found_play = False
        for row in edited.buttons:
            for btn in row:
                btn_text = btn.text.strip()
                if btn_text in ("🎮Играть матч", "🎮 Играть матч"):
                    await edited.click(text=btn_text)
                    found_play = True
                    break
            if found_play:
                break

        if not found_play:
            await self.client.send_message(chat, "<b>Ошибка:</b> не найдена кнопка '🎮Играть матч'.")
            return

        # Успешно
        await self.client.send_message(chat, "<b>✅ Готово:</b> нажаты «⚽️Матч» и «🎮Играть матч».")
