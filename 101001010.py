# scope: hikka_only
# meta developer: @d4n13lxx
# name: FCardAutoMatchAndPlay

from .. import loader, utils
from hikkatl.tl.custom import MessageButton


@loader.tds
class FCardAutoMatchAndPlayMod(loader.Module):
    """Автоматическое нажатие кнопок 'Матч' и 'Играть матч' в @F_CardBot"""

    strings = {
        "name": "FCardAutoMatchAndPlay",
        "sending_menu": "✅ Отправлено 'Меню'. Ожидание кнопок...",
        "clicking_match_button": "🎮 Нажата кнопка 'Матч'",
        "clicking_play_button": "⚽️ Нажата кнопка 'Играть матч'",
        "play_count": "🔁 Нажато {} раз",
        "done": "✅ Завершено. Нажато 5 раз.",
    }

    async def client_ready(self, client, db):
        self._client = client

    async def менюcmd(self, message):
        """Отправить 'Меню', нажать 'Матч' и затем 5 раз 'Играть матч'"""
        bot_username = "@F_CardBot"

        # Отправляем сообщение "Меню"
        await self._client.send_message(bot_username, "Меню")
        await utils.answer(message, self.strings["sending_menu"])

        # Шаг 1: Ждём ответное сообщение с кнопкой "Матч"
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
                        break
            else:
                return await utils.answer(message, "❌ Кнопка 'Матч' не найдена")

            # Шаг 2: Ждём ответное сообщение с кнопкой "Играть матч"
            play_response = await self._client.get_messages(bot_username, limit=1)
            if not play_response:
                return await utils.answer(message, "❌ Не получил ответ после нажатия 'Матч'")

            play_response = play_response[0]
            if not play_response.buttons:
                return await utils.answer(message, "❌ В ответе нет кнопок после 'Матч'")

            # Ищем кнопку "Играть матч"
            play_button = None
            for row in play_response.buttons:
                for button in row:
                    if isinstance(button, MessageButton) and button.text == "Играть матч":
                        play_button = button
                        break
                if play_button:
                    break

            if not play_button:
                return await utils.answer(message, "❌ Кнопка 'Играть матч' не найдена")

            # Шаг 3: Нажимаем "Играть матч" 5 раз
            count = 0
            while count < 5:
                await play_button.click()
                count += 1
                await utils.answer(message, self.strings["play_count"].format(count))
                await asyncio.sleep(1)  # Пауза между нажатиями (можно убрать)

            await utils.answer(message, self.strings["done"])

        except Exception as e:
            await utils.answer(message, f"❌ Произошла ошибка: {e}")