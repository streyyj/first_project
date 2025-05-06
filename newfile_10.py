# scope: hikka_only
# meta developer: @d4n13lxx
# name: FCardAutoMatchAndRating

from .. import loader, utils
from hikkatl.tl.custom import MessageButton
from hikkatl import events
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
        "timeout_error": "⏳ Время ожидания истекло. Бот не ответил."
    }

    async def client_ready(self, client, db):
        self._client = client

    async def менюcmd(self, message):
        """Отправить 'Меню', нажать 'Матч', 'Играть матч' и затем 'Рейтинг'"""
        bot_username = "@F_CardBot"
        timeout = 10  # секунд ожидания ответа от бота

        await utils.answer(message, self.strings["sending_menu"])
        await self._client.send_message(bot_username, "Меню")

        try:
            # 🔁 Шаг 1: Ждём сообщение после команды "Меню"
            response = await self._wait_for_new_message(bot_username, timeout)
            if not response or not response.buttons:
                return await utils.answer(message, f"❌ Кнопки не найдены. Сообщение: {response.text if response else 'Нет ответа'}")

            # 🔘 Нажимаем "Матч"
            match_button = self._find_button(response, "Матч")
            if not match_button:
                return await utils.answer(message, "❌ Кнопка 'Матч' не найдена")
            await match_button.click()
            await utils.answer(message, self.strings["clicking_match_button"])

            # 🔁 Шаг 2: Ждём сообщение после "Матч"
            play_response = await self._wait_for_new_message(bot_username, timeout)
            if not play_response or not play_response.buttons:
                return await utils.answer(message, f"❌ Кнопки не найдены. Сообщение: {play_response.text if play_response else 'Нет ответа'}")

            # 🔘 Нажимаем "Играть матч"
            play_button = self._find_button(play_response, "Играть матч")
            if not play_button:
                return await utils.answer(message, "❌ Кнопка 'Играть матч' не найдена")
            await play_button.click()
            await utils.answer(message, self.strings["clicking_play_button"])

            # 🔁 Шаг 3: Ждём сообщение после "Играть матч"
            rating_response = await self._wait_for_new_message(bot_username, timeout)
            if not rating_response or not rating_response.buttons:
                return await utils.answer(message, f"❌ Кнопки не найдены. Сообщение: {rating_response.text if rating_response else 'Нет ответа'}")

            # 🔘 Нажимаем "Рейтинг"
            rating_button = self._find_button(rating_response, "Рейтинг")
            if not rating_button:
                return await utils.answer(message, "❌ Кнопка 'Рейтинг' не найдена")
            await rating_button.click()
            await utils.answer(message, self.strings["clicking_rating_button"])

            await utils.answer(message, self.strings["done"])

        except asyncio.TimeoutError:
            await utils.answer(message, self.strings["timeout_error"])
        except Exception as e:
            await utils.answer(message, f"❌ Ошибка: {e}")

    async def _wait_for_new_message(self, bot_username, timeout):
        """Ждёт новое сообщение от указанного бота"""
        event = await self._client.wait_for(
            events.NewMessage(from_users=bot_username),
            timeout=timeout
        )
        return event.message

    def _find_button(self, message, keyword):
        """Находит первую кнопку, содержащую ключевое слово"""
        if not message.buttons:
            return None
        for row in message.buttons:
            for btn in row:
                if isinstance(btn, MessageButton) and keyword in btn.text:
                    return btn
        return None