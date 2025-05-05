# scope: hikka_only
# meta developer: @d4n13lxx
# name: FCardAutoPlay

from .. import loader, utils
from hikkatl.tl.custom import MessageButton

@loader.tds
class FCardAutoPlay(loader.Module):
    """Автоматическое нажатие кнопки 'Играть матч'"""

    async def client_ready(self, client, db):
        self._client = client

    async def watcher(self, message):
        # Проверяем, что сообщение от @F_CardBot
        if getattr(message, "sender", None) and (await message.get_sender()).username == "F_CardBot":
            # Если есть кнопки
            if message.buttons:
                for row in message.buttons:
                    for button in row:
                        if isinstance(button, MessageButton) and button.text == "Играть матч":
                            await button.click()
                            await self._client.send_message(
                                message.chat.id,
                                "🎮 Кнопка 'Играть матч' нажата!"
                            )