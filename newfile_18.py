# scope: hikka_only
# meta developer: @d4n13lxx
# name: FCardShowButtons

from .. import loader, utils
from hikkatl.tl.custom import MessageButton

@loader.tds
class FCardShowButtonsMod(loader.Module):
    """Выводит названия всех кнопок из последнего сообщения от @F_CardBot"""

    strings = {
        "name": "FCardShowButtons",
        "no_buttons": "❌ В последнем сообщении нет кнопок.",
        "buttons_list": "ButtonTitles:\n{}",
        "no_message": "❌ Не получил сообщений от @F_CardBot",
    }

    async def client_ready(self, client, db):
        self._client = client

    async def кнопкиcmd(self, message):
        """Показать все кнопки из последнего сообщения от @F_CardBot"""
        bot_username = "@F_CardBot"

        # Получаем последнее сообщение от бота
        messages = await self._client.get_messages(bot_username, limit=1)
        if not messages:
            return await utils.answer(message, self.strings["no_message"])

        msg = messages[0]

        # Проверяем, есть ли кнопки
        if not msg.buttons:
            return await utils.answer(message, self.strings["no_buttons"])

        # Собираем текст кнопок
        buttons_text = []
        for row in msg.buttons:
            for btn in row:
                if isinstance(btn, MessageButton):
                    buttons_text.append(f"▫️ {btn.text}")

        # Отвечаем списком кнопок под исходным сообщением
        await utils.answer(message, self.strings["buttons_list"].format("\n".join(buttons_text)))