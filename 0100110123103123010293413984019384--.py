import asyncio
from telethon import events
from .. import loader

@loader.tds
class FootCardPlayMod(loader.Module):
    """Auto-play match in FootCardBot (@F_CardBot)"""

    strings = {"name": "FootCardAutoMatch"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.unrestricted
    async def fcplaycmd(self, message):
        """
        Использование: .fcplay
        Автоматически отправляет «Меню», кликает «⚽️ Матч» и затем «🎮 Играть матч» у бота @F_CardBot.
        """
        chat = await message.get_chat()
        chat_id = chat.id

        # 1) Отправляем "Меню"
        await self.client.send_message(chat_id, "Меню")
        await asyncio.sleep(0.2)

        # 2) Ждём сообщение от бота
        try:
            resp = await self.client.wait_event(
                events.NewMessage(
                    chats=chat_id,
                    from_users="F_CardBot"
                ),
                timeout=5
            )
        except asyncio.TimeoutError:
            await message.edit("❗️ Не пришёл ответ на 'Меню' от @F_CardBot.")
            return

        # 3) Ищем кнопку «⚽️ Матч»
        match_button = None
        for row in resp.buttons or []:
            for btn in row:
                if btn.text.strip() == "⚽️ Матч":
                    match_button = btn
                    break
            if match_button:
                break

        if not match_button:
            await message.edit("❗️ Не найдена кнопка «⚽️ Матч» у сообщения бота.")
            return

        await resp.click(text="⚽️ Матч")
        await asyncio.sleep(0.5)

        # 4) Ждём новое сообщение с кнопкой «🎮 Играть матч»
        try:
            match_msg = await self.client.wait_event(
                events.NewMessage(
                    chats=chat_id,
                    from_users="F_CardBot"
                ),
                timeout=5
            )
        except asyncio.TimeoutError:
            await message.edit("❗️ Бот не ответил после клика по «⚽️ Матч».")
            return

        # 5) Ищем кнопку «🎮 Играть матч»
        play_button = None
        for row in match_msg.buttons or []:
            for btn in row:
                if btn.text.strip() == "🎮 Играть матч":
                    play_button = btn
                    break
            if play_button:
                break

        if not play_button:
            await message.edit("❗️ Не найдена кнопка «🎮 Играть матч» у сообщения.")
            return

        await match_msg.click(text="🎮 Играть матч")
        await message.delete()