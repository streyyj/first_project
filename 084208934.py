# scope: hikka_only
# meta developer: @d4n13lxx
# name: FCardAutoMatch

from .. import loader, utils
from hikkatl.tl.custom import MessageButton


@loader.tds
class FCardAutoMatchMod(loader.Module):
    """Автоматическое нажатие кнопки 'Матч' в @F_CardBot"""

    strings = {
        "name": "FCardAutoMatch",
        "sending_menu": "✅ Отправлено 'Меню'. Ожидание кнопок...",
        "clicking_match_button": "🎮 Нажата кнопка 'Матч'",
    }

    async def client_ready(self, client, db):
        self._client = client

    async def менюcmd(self, message):
        """Отправить 'Меню' и нажать кнопку 'Матч'"""
        bot_username = "@F_CardBot"

        # Отправляем сообщение "Меню"
        await self._client.send_message(bot_username, "Меню")
        await utils.answer(message, self.strings["sending_menu"])

        # Ждём ответное сообщение с кнопками
        try:
            response = await self._client.get_messages(bot_username, limit=1)
            if not response:
                return await utils.answer(message, "❌ Не получил ответ от бота")

            response = response[0]
            if not response.buttons:
                return await utils.answer(message, "❌ В ответе нет кнопок")

            # Ищем кнопку "Матч"
            for row in response.buttons:
                for button in row:
                    if isinstance(button, MessageButton) and button.text == "⚽️ Матч":
                        await button.click()
                        await utils.answer(message, self.strings["clicking_match_button"])
                        return

            await utils.answer(message, "❌ Кнопка 'Матч' не найдена")
        except Exception as e:
            await utils.answer(message, f"❌ Произошла ошибка: {e}")