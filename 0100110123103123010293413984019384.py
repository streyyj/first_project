from telethon import events
from .. import loader
import asyncio

@loader.tds
class FootCardPlayMod(loader.Module):
    """Auto-play match in FootCardBot (@F_CardBot)"""

    strings = {"name": "FootCardAutoMatch"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.unrestricted
    async def fcplaycmd(self, message):
        """
        .fcplay — Автоматически кликает «⚽️ Матч» → «🎮 Играть матч» у @F_CardBot
        """
        chat = await message.get_chat()
        chat_id = chat.id

        # 1. Отправляем "Меню"
        await self.client.send_message(chat_id, "Меню")
        await asyncio.sleep(0.3)  # дожидаемся появления ответа

        # 2. Ждём ответа от бота
        try:
            resp = await self.client.wait_event(
                events.NewMessage(chats=chat_id, from_users="F_CardBot"),
                timeout=5
            )
        except Exception:
            await message.edit("❗️ Не пришёл ответ на 'Меню' от @F_CardBot.")
            return

        if not hasattr(resp, "buttons") or resp.buttons is None:
            await message.edit("❗️ Нет кнопок в сообщении от бота.")
            return

        # 3. Ищем и нажимаем кнопку «⚽️ Матч»
        for row in resp.buttons:
            for btn in row:
                if btn.text == "⚽️ Матч":
                    await resp.click(text=btn.text)
                    break
            else:
                continue
            break
        else:
            await message.edit("❗️ Кнопка '⚽️ Матч' не найдена.")
            return

        # 4. Ждём редактированного сообщения с новой клавиатурой
        try:
            edited = await self.client.wait_event(
                events.MessageEdited(chats=chat_id, from_users="F_CardBot", msg_id=resp.id),
                timeout=5
            )
        except Exception:
            await message.edit("❗️ Не дождались редактирования после нажатия '⚽️ Матч'.")
            return

        if not hasattr(edited, "buttons") or edited.buttons is None:
            await message.edit("❗️ Нет кнопок после редактирования.")
            return

        # 5. Ищем и нажимаем кнопку «🎮 Играть матч»
        for row in edited.buttons:
            for btn in row:
                if btn.text == "🎮 Играть матч":
                    await edited.click(text=btn.text)
                    await message.delete()
                    return

        await message.edit("❗️ Кнопка '🎮 Играть матч' не найдена.")