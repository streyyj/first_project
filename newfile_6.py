# meta developer: @F_CardBot
# requires: hikka
# version: 1.0

from hikka import loader, utils
from hikka.types import Message

@loader.module("MenuSender", "F_CardBot")
class MenuSender(loader.Module):
    """Отправляет команду 'Меню' в бота @F_CardBot"""

    async def menucmd(self, message: Message):
        """Отправить 'Меню' в бота"""
        try:
            # Отправляем сообщение боту
            await self.client.send_message(
                "F_CardBot",  # Username бота без @
                "Меню"        # Сообщение для отправки
            )
            await utils.answer(message, "✅ Сообщение 'Меню' успешно отправлено в бота")
        except Exception as e:
            await utils.answer(message, f"❌ Ошибка при отправке: {str(e)}")