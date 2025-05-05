from hikkatl.tl.functions.messages import SendMessageRequest
from hikkatl.utils import get_display_name
from .. import loader, utils

@loader.tds
class FCardMenuMod(loader.Module):
    """Модуль для вызова меню в боте @F_CardBot"""
    strings = {"name": "FCardMenu"}

    async def fcardcmd(self, message):
        """Отправить команду для вызова меню (пример: .fcard)"""
        bot_username = "@F_CardBot"
        await self.client(SendMessageRequest(bot_username, "/start"))
        await utils.answer(message, "Команда отправлена. Проверьте диалог с ботом.")