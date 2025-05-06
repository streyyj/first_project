# scope: hikka_only
# meta developer: @d4n13lxx
# name: FCardShowButtons

from .. import loader, utils
from hikkatl.tl.custom import MessageButton
import asyncio

@loader.tds
class FCardShowButtonsMod(loader.Module):
    """Выводит названия всех кнопок из последнего сообщения от @F_CardBot"""

    strings = {
        "name": "FCardShowButtons",
        "no_buttons": "❌ В последнем сообщении нет кнопок.",
        "buttons_list": "ButtonTitles:\n{}",
        "no_message": "❌ Не получил сообщений от @F_CardBot",
        "timeout_error": "⏳ Время ожидания истекло. Бот не ответил.",
        "debug_info": "🔍 Отладочная информация:\nMessage text: {}\nButtons: {}"
    }

    async def client_ready(self, client, db):
        self._client = client

    async def кнопкиcmd(self, message):
        """Показать все кнопки из последнего сообщения от @F_CardBot"""
        bot_username = "@F_CardBot"
        timeout = 10  # секунд ожидания ответа от бота
        attempts = 20  # количество попыток получить новое сообщение

        try:
            # 🔁 Ожидаем новое сообщение от бота
            response = await self._wait_for_new_message(bot_username, timeout, attempts)
            if not response:
                return await utils.answer(message, self.strings["no_message"])

            # Проверяем наличие кнопок
            if not response.buttons:
                return await utils.answer(message, self.strings["no_buttons"])

            # Собираем текст кнопок
            buttons_text = []
            for row in response.buttons:
                for btn in row:
                    if isinstance(btn, MessageButton):
                        buttons_text.append(f"▫️ {btn.text}")

            # Отвечаем списком кнопок под исходным сообщением
            await utils.answer(
                message,
                self.strings["buttons_list"].format("\n".join(buttons_text))
            )

        except asyncio.TimeoutError:
            await utils.answer(message, self.strings["timeout_error"])
        except Exception as e:
            await utils.answer(message, f"❌ Произошла ошибка: {e}")

    async def _wait_for_new_message(self, bot_username, timeout, attempts):
        """Ждёт новое сообщение от указанного бота"""
        delay = timeout / attempts
        for _ in range(attempts):
            await asyncio.sleep(delay)
            msgs = await self._client.get_messages(bot_username, limit=1)
            if msgs:
                return msgs[0]
        raise asyncio.TimeoutError()