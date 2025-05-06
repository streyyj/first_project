# scope: hikka_only
# meta developer: @d4n13lxx
# name: FCardAutoMatchAndRating

from .. import loader, utils
from hikkatl.tl.custom import MessageButton
import asyncio

@loader.tds
class FCardAutoMatchAndRatingMod(loader.Module):
    """Автоматическое нажатие кнопок 'Матч', 'Играть матч' и 'Рейтинг' в @F_CardBot"""

    strings = {
        "name": "FCardAutoMatchAndRating",
        "sending_menu": "✅ Отправлено 'Меню'. Ожидание кнопок...",
        "clicking_match_button": "🎮 Нажата кнопка 'Матч'",
        "clicking_play_button": "⚽️ Нажата кнопка 'Играть матч'",
        "clicking_rating_button": "🏆 Нажата кнопка 'Рейтинг'",
        "done": "✅ Завершено.",
    }

    async def client_ready(self, client, db):
        self._client = client

    async def менюcmd(self, message):
        """Отправить 'Меню', нажать 'Матч', 'Играть матч' и затем 'Рейтинг'"""
        bot_username = "@F_CardBot"

        # Шаг 0: Отправляем сообщение "Меню"
        await self._client.send_message(bot_username, "Меню")
        await utils.answer(message, self.strings["sending_menu"])

        # Ждём ответ
        await asyncio.sleep(1)

        # Шаг 1: Ищем кнопку "Матч"
        try:
            response = await self._client.get_messages(bot_username, limit=1)
            if not response:
                return await utils.answer(message, "❌ Не получил ответ от бота")
            response = response[0]

            if not response.buttons:
                return await utils.answer(message, f"❌ Кнопки не найдены. Сообщение: {response.text}")

            match_button = None
            for row in response.buttons:
                for btn in row:
                    if isinstance(btn, MessageButton) and "Матч" in btn.text:
                        match_button = btn
                        break
                if match_button:
                    break

            if not match_button:
                return await utils.answer(message, "❌ Кнопка 'Матч' не найдена")

            await match_button.click()
            await utils.answer(message, self.strings["clicking_match_button"])
            await asyncio.sleep(1)

            # Шаг 2: Ищем кнопку "Играть матч"
            play_response = await self._client.get_messages(bot_username, limit=1)
            if not play_response:
                return await utils.answer(message, "❌ Не получил ответ после 'Матч'")
            play_response = play_response[0]

            if not play_response.buttons:
                return await utils.answer(message, f"❌ Кнопки не найдены. Сообщение: {play_response.text}")

            play_button = None
            for row in play_response.buttons:
                for btn in row:
                    if isinstance(btn, MessageButton) and "Играть матч" in btn.text:
                        play_button = btn
                        break
                if play_button:
                    break

            if not play_button:
                return await utils.answer(message, "❌ Кнопка 'Играть матч' не найдена")

            await play_button.click()
            await utils.answer(message, self.strings["clicking_play_button"])
            await asyncio.sleep(1)

            # Шаг 3: Ищем кнопку "Рейтинг"
            rating_response = await self._client.get_messages(bot_username, limit=1)
            if not rating_response:
                return await utils.answer(message, "❌ Не получил ответ после 'Играть матч'")
            rating_response = rating_response[0]

            if not rating_response.buttons:
                return await utils.answer(message, f"❌ Кнопки не найдены. Сообщение: {rating_response.text}")

            rating_button = None
            for row in rating_response.buttons:
                for btn in row:
                    if isinstance(btn, MessageButton) and "Рейтинг" in btn.text:
                        rating_button = btn
                        break
                if rating_button:
                    break

            if not rating_button:
                return await utils.answer(message, "❌ Кнопка 'Рейтинг' не найдена")

            await rating_button.click()
            await utils.answer(message, self.strings["clicking_rating_button"])

            await utils.answer(message, self.strings["done"])

        except Exception as e:
            await utils.answer(message, f"❌ Произошла ошибка: {e}")