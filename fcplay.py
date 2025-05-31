import asyncio
from telethon import events
from .. import loader

@loader.tds
class FootCardPlayMod(loader.Module):
    """Auto-play match в FootCardBot (@F_CardBot) для Hikka-userbot"""

    strings = {"name": "FootCardAutoMatch"}

    async def client_ready(self, client, db):
        # сохраняем обёрнутый Hikka‑клиент и «сырый» Telethon-клиент
        self._wrapped_client = client            # CustomTelegramClient (Hikka)
        self._telethon_client = client._client    # чистый TelethonClient

    @loader.unrestricted
    async def fcplaycmd(self, message):
        """
        .fcplay  —  автоматический игровой модуль для @F_CardBot:
           1) отправляет «Меню»
           2) кликает кнопку «⚽️ Матч»
           3) кликает кнопку «🎮 Играть матч»
        """
        chat = await message.get_chat()
        chat_id = chat.id
        tclient = self._telethon_client  # ссылка на сырой TelethonClient

        # 1) Отправляем «Меню»
        await self._wrapped_client.send_message(chat_id, "Меню")
        await asyncio.sleep(0.3)

        # 2) Ждём любого нового сообщения от @F_CardBot
        try:
            resp_event = await tclient.wait_event(
                events.NewMessage(
                    chats=chat_id,
                    from_users="F_CardBot"
                ),
                timeout=5
            )
        except asyncio.TimeoutError:
            await message.edit("❗️ Не пришёл ответ на «Меню» от @F_CardBot.")
            return

        # Если нет кнопок — выходим
        buttons = getattr(resp_event, "buttons", None)
        if not buttons:
            await message.edit("❗️ В ответе от бота нет inline‑кнопок.")
            return

        # 3) Ищем кнопку «⚽️ Матч» и кликаем
        match_btn = None
        for row in buttons:
            for btn in row:
                if btn.text.strip() == "⚽️ Матч":
                    match_btn = btn
                    break
            if match_btn:
                break

        if not match_btn:
            await message.edit("❗️ Кнопка «⚽️ Матч» не найдена.")
            return

        # кликаем
        await resp_event.click(text=match_btn.text)
        await asyncio.sleep(0.5)

        # 4) После клика бот может ответить либо новым сообщением, либо отредактировать старое.
        #    Поэтому ждём и NewMessage, и MessageEdited.
        try:
            next_event = await tclient.wait_event(
                lambda e: (
                    isinstance(e, (events.NewMessage, events.MessageEdited))
                    and e.chat_id == chat_id
                    and e.sender_id == (await tclient.get_entity("F_CardBot")).id
                ),
                timeout=5
            )
        except asyncio.TimeoutError:
            await message.edit("❗️ Бот не прислал новую клавиатуру после «⚽️ Матч».")
            return

        # 5) Ищем кнопку «🎮 Играть матч» в обновлённом сообщении
        buttons2 = getattr(next_event, "buttons", None)
        if not buttons2:
            await message.edit("❗️ В обновлённом сообщении нет кнопок.")
            return

        play_btn = None
        for row in buttons2:
            for btn in row:
                if btn.text.strip() == "🎮 Играть матч":
                    play_btn = btn
                    break
            if play_btn:
                break

        if not play_btn:
            await message.edit("❗️ Кнопка «🎮 Играть матч» не найдена.")
            return

        # кликаем «Играть матч»
        await next_event.click(text=play_btn.text)

        # удаляем команду, чтобы не засорять чат
        await message.delete()